import httpx
import pytest

from config.settings import settings
from services import rate_limiter


@pytest.fixture
def upstash(monkeypatch):
    """
    Enable rate limiting against an in-memory fake of Upstash.
    """

    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_URL", "https://fake.upstash.io")
    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_TOKEN", "token")
    monkeypatch.setattr(settings, "RATE_LIMIT_REQUESTS", 2)

    counts: dict[str, int] = {}

    async def fake_increment(key: str, window_seconds: int) -> int:
        counts[key] = counts.get(key, 0) + 1
        return counts[key]

    monkeypatch.setattr(rate_limiter, "_increment", fake_increment)

    return counts


def upload(client, pdf_bytes, ip="1.2.3.4"):
    return client.post(
        "/analyze",
        files={"file": ("doc.pdf", pdf_bytes, "application/pdf")},
        headers={"X-Forwarded-For": f"{ip}, 10.0.0.1"},
    )


def test_blocks_after_limit(client, pdf_bytes, fake_pipeline, upstash):
    assert upload(client, pdf_bytes).status_code == 200
    assert upload(client, pdf_bytes).status_code == 200

    response = upload(client, pdf_bytes)

    assert response.status_code == 429
    assert "limit of 2 analyses" in response.json()["error"]
    assert int(response.headers["Retry-After"]) > 0
    assert len(fake_pipeline) == 2


def test_limits_each_ip_separately(client, pdf_bytes, fake_pipeline, upstash):
    upload(client, pdf_bytes, ip="1.1.1.1")
    upload(client, pdf_bytes, ip="1.1.1.1")

    assert upload(client, pdf_bytes, ip="2.2.2.2").status_code == 200


def test_allows_requests_when_not_configured(client, pdf_bytes, fake_pipeline, monkeypatch):
    monkeypatch.setattr(settings, "RATE_LIMIT_REQUESTS", 0)

    assert upload(client, pdf_bytes).status_code == 200


def test_fails_open_when_upstash_is_down(client, pdf_bytes, fake_pipeline, monkeypatch):
    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_URL", "https://fake.upstash.io")
    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_TOKEN", "token")
    monkeypatch.setattr(settings, "RATE_LIMIT_REQUESTS", 0)

    async def broken_increment(key: str, window_seconds: int) -> int:
        raise httpx.ConnectError("down")

    monkeypatch.setattr(rate_limiter, "_increment", broken_increment)

    assert upload(client, pdf_bytes).status_code == 200


@pytest.mark.anyio
async def test_increment_sends_incr_and_expire(monkeypatch):
    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_URL", "https://fake.upstash.io")
    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_TOKEN", "token")
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["auth"] = request.headers["Authorization"]
        seen["body"] = request.read()
        return httpx.Response(200, json=[{"result": 3}, {"result": 1}])

    real_client = httpx.AsyncClient
    monkeypatch.setattr(
        rate_limiter.httpx,
        "AsyncClient",
        lambda **kwargs: real_client(transport=httpx.MockTransport(handler), **kwargs),
    )

    assert await rate_limiter._increment("ratelimit:test", 3600) == 3
    assert seen["url"] == "https://fake.upstash.io/pipeline"
    assert seen["auth"] == "Bearer token"
    assert b'["INCR","ratelimit:test"]' in seen["body"]
    assert b'["EXPIRE","ratelimit:test","3600","NX"]' in seen["body"]


@pytest.fixture
def anyio_backend():
    return "asyncio"
