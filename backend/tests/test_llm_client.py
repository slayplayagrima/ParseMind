from types import SimpleNamespace

import httpx
import pytest
from groq import RateLimitError

from config.settings import settings
from services import llm_client


@pytest.fixture
def fake_groq(monkeypatch):
    """
    Swap the Groq client for a fake whose reply each test controls.
    """

    state = {"reply": "ok", "error": None, "calls": 0}

    def create(**kwargs):
        state["calls"] += 1
        if state["error"]:
            raise state["error"]
        message = SimpleNamespace(content=state["reply"])
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])

    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    monkeypatch.setattr(llm_client, "get_client", lambda: client)

    return state


def test_client_uses_timeout_and_retries(monkeypatch):
    monkeypatch.setattr(llm_client, "API_KEY", "test-key")
    monkeypatch.setattr(llm_client, "_client", None)
    monkeypatch.setattr(settings, "LLM_TIMEOUT_SECONDS", 12.0)
    monkeypatch.setattr(settings, "LLM_MAX_RETRIES", 4)

    client = llm_client.get_client()

    assert client.timeout == 12.0
    assert client.max_retries == 4


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.setattr(llm_client, "API_KEY", "")
    monkeypatch.setattr(llm_client, "_client", None)

    with pytest.raises(RuntimeError, match="GROQ_API_KEY is missing"):
        llm_client.get_client()


def test_text_response(fake_groq):
    fake_groq["reply"] = "  A short summary.  "

    assert llm_client.generate_text_response("summarize") == "A short summary."


def test_json_response_strips_markdown_fences(fake_groq):
    fake_groq["reply"] = '```json\n{"workflow": "contract_workflow"}\n```'

    assert llm_client.generate_json_response("classify") == {"workflow": "contract_workflow"}


def test_invalid_json_raises_value_error(fake_groq):
    fake_groq["reply"] = "not json"

    with pytest.raises(ValueError, match="Invalid JSON"):
        llm_client.generate_json_response("classify")


def test_empty_reply_is_an_error(fake_groq):
    fake_groq["reply"] = ""

    with pytest.raises(RuntimeError, match="LLM request failed"):
        llm_client.generate_text_response("summarize")


def test_rate_limit_is_mapped(fake_groq):
    request = httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions")
    fake_groq["error"] = RateLimitError(
        "Rate limit reached",
        response=httpx.Response(429, request=request),
        body=None,
    )

    with pytest.raises(RuntimeError, match="RATE_LIMIT_EXCEEDED"):
        llm_client.generate_text_response("summarize")


def test_rate_limit_returns_429_to_user(pdf_bytes, monkeypatch):
    from fastapi.testclient import TestClient

    from app.api import routes
    from app.main import app

    def limited(_: bytes):
        raise RuntimeError("RATE_LIMIT_EXCEEDED")

    monkeypatch.setattr(routes, "process_document", limited)

    response = TestClient(app, raise_server_exceptions=False).post(
        "/analyze",
        files={"file": ("doc.pdf", pdf_bytes, "application/pdf")},
    )

    assert response.status_code == 429
    assert "rate limit" in response.json()["error"]
