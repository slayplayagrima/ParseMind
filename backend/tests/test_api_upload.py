from config.settings import settings
from services.errors import DocumentError


def upload(client, data: bytes, content_type: str = "application/pdf", name: str = "doc.pdf"):
    return client.post("/analyze", files={"file": (name, data, content_type)})


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}


def test_valid_pdf_is_analyzed(client, pdf_bytes, fake_pipeline):
    response = upload(client, pdf_bytes)

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert fake_pipeline == [pdf_bytes]


def test_rejects_non_pdf_content_type(client, fake_pipeline):
    response = upload(client, b"hello", content_type="text/plain", name="notes.txt")

    assert response.status_code == 400
    assert response.json()["error"] == "Only PDF files are supported."
    assert fake_pipeline == []


def test_rejects_file_without_pdf_signature(client, fake_pipeline):
    response = upload(client, b"not really a pdf")

    assert response.status_code == 400
    assert response.json()["error"] == "The uploaded file is not a valid PDF."
    assert fake_pipeline == []


def test_rejects_oversized_upload(client, monkeypatch, fake_pipeline):
    monkeypatch.setattr(settings, "MAX_UPLOAD_MB", 1)
    too_big = b"%PDF-" + b"0" * (1024 * 1024)

    response = upload(client, too_big)

    assert response.status_code == 413
    assert "1 MB" in response.json()["error"]
    assert fake_pipeline == []


def test_document_error_is_shown_to_user(client, pdf_bytes, monkeypatch):
    from app.api import routes

    def reject(_: bytes):
        raise DocumentError("Password-protected PDFs are not supported.")

    monkeypatch.setattr(routes, "process_document", reject)

    response = upload(client, pdf_bytes)

    assert response.status_code == 400
    assert response.json() == {
        "success": False,
        "data": None,
        "error": "Password-protected PDFs are not supported.",
    }


def test_unexpected_error_stays_generic(pdf_bytes, monkeypatch):
    from fastapi.testclient import TestClient

    from app.api import routes
    from app.main import app

    client = TestClient(app, raise_server_exceptions=False)

    def crash(_: bytes):
        raise RuntimeError("secret internal detail")

    monkeypatch.setattr(routes, "process_document", crash)

    response = upload(client, pdf_bytes)

    assert response.status_code == 500
    assert response.json()["error"] == "Internal server error."
