import os

# Settings require a Groq key at import time. Tests never call Groq,
# so a placeholder is enough. Must be set before the app is imported.
os.environ.setdefault("GROQ_API_KEY", "test-key")

import fitz
import pytest
from fastapi.testclient import TestClient

from app.api import routes
from app.main import app
from config.settings import settings


def make_pdf(pages: int = 1, text: str = "This Agreement is made between Acme and Beta.") -> bytes:
    """
    Build a small text PDF in memory.
    """

    document = fitz.open()

    for _ in range(pages):
        page = document.new_page()
        page.insert_text((72, 72), text)

    data = document.tobytes()
    document.close()

    return data


@pytest.fixture
def pdf_bytes() -> bytes:
    return make_pdf()


@pytest.fixture(autouse=True)
def no_rate_limit(monkeypatch):
    """
    Keep tests offline: Upstash is never called unless a test opts in.
    """

    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_URL", "")
    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_TOKEN", "")


@pytest.fixture
def fake_pipeline(monkeypatch):
    """
    Replace the Groq-backed pipeline with a stub that records its input.
    """

    calls = []

    def fake_process_document(data: bytes):
        calls.append(data)
        return {"workflow": "contract_workflow"}

    monkeypatch.setattr(routes, "process_document", fake_process_document)

    return calls


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
