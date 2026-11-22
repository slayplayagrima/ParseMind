import json
from urllib.parse import parse_qs

import fitz
import httpx
import pytest

from config.settings import settings
from services import ocr_service, pdf_service
from services.errors import DocumentError
from services.pdf_service import extract_text_from_pdf


def make_scanned_pdf(pages: int = 1) -> bytes:
    """
    A PDF whose pages hold only an image, like a scan: no text layer.
    """

    document = fitz.open()
    image = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 60, 60), False)
    image.clear_with(200)

    for _ in range(pages):
        page = document.new_page()
        page.insert_image(fitz.Rect(72, 72, 300, 300), pixmap=image)

    data = document.tobytes()
    document.close()

    return data


@pytest.fixture
def ocr_api(monkeypatch):
    """
    Turn OCR on and answer OCR.space requests from a local fake.
    Each test sets the reply; every request is recorded.
    """

    state = {"requests": [], "reply": None, "status": 200}

    def handler(request: httpx.Request) -> httpx.Response:
        form = {key: values[0] for key, values in parse_qs(request.content.decode()).items()}
        state["requests"].append({"headers": request.headers, "form": form})

        reply = state["reply"]
        if callable(reply):
            reply = reply(len(state["requests"]))

        return httpx.Response(state["status"], content=json.dumps(reply))

    monkeypatch.setattr(settings, "OCR_SPACE_API_KEY", "ocr-test-key")
    monkeypatch.setattr(
        ocr_service, "_client", lambda: httpx.Client(transport=httpx.MockTransport(handler))
    )

    return state


def ok(text: str) -> dict:
    return {
        "IsErroredOnProcessing": False,
        "ParsedResults": [{"ParsedText": text, "FileParseExitCode": 1}],
    }


def test_scanned_pdf_without_ocr_key_explains_the_problem(monkeypatch):
    monkeypatch.setattr(settings, "OCR_SPACE_API_KEY", "")

    with pytest.raises(DocumentError, match="may be scanned"):
        extract_text_from_pdf(make_scanned_pdf())


def test_scanned_pdf_is_read_with_ocr(ocr_api):
    ocr_api["reply"] = ok("INVOICE INV-9\r\nTotal:   $500")

    text = extract_text_from_pdf(make_scanned_pdf())

    assert text == "INVOICE INV-9\nTotal: $500"

    request = ocr_api["requests"][0]
    assert request["headers"]["apikey"] == "ocr-test-key"
    assert request["form"]["base64Image"].startswith("data:image/jpeg;base64,")
    assert request["form"]["OCREngine"] == "2"
    assert request["form"]["language"] == "eng"


def test_each_page_is_sent_and_kept_in_order(ocr_api):
    ocr_api["reply"] = lambda n: ok(f"page {n}")

    text = extract_text_from_pdf(make_scanned_pdf(pages=3))

    assert len(ocr_api["requests"]) == 3
    # Requests run in parallel, so check every page came back once.
    assert sorted(text.split("\n\n")) == ["page 1", "page 2", "page 3"]


def test_text_pdfs_never_call_ocr(ocr_api):
    from tests.conftest import make_pdf

    assert "Acme" in extract_text_from_pdf(make_pdf())
    assert ocr_api["requests"] == []


def test_scanned_page_limit(ocr_api, monkeypatch):
    monkeypatch.setattr(settings, "OCR_MAX_PAGES", 2)

    with pytest.raises(DocumentError, match="up to 2 pages"):
        extract_text_from_pdf(make_scanned_pdf(pages=3))

    assert ocr_api["requests"] == []


@pytest.mark.parametrize(
    ("status", "reply"),
    [
        (200, {"IsErroredOnProcessing": True, "ErrorMessage": ["File too large"]}),
        (500, {"error": "server down"}),
        (403, {"error": "bad key"}),
    ],
)
def test_ocr_failures_become_a_friendly_error(ocr_api, status, reply):
    ocr_api["status"] = status
    ocr_api["reply"] = reply

    with pytest.raises(DocumentError, match="couldn't read this scanned document"):
        extract_text_from_pdf(make_scanned_pdf())


def test_ocr_that_finds_no_text_is_reported(ocr_api):
    ocr_api["reply"] = ok("   ")

    with pytest.raises(DocumentError, match="No readable text"):
        extract_text_from_pdf(make_scanned_pdf())


def test_large_pages_are_shrunk_under_the_upload_limit(monkeypatch):
    sizes = []
    real_get_pixmap = fitz.Page.get_pixmap

    def tracking_get_pixmap(self, *args, **kwargs):
        pixmap = real_get_pixmap(self, *args, **kwargs)
        sizes.append(kwargs["dpi"])
        return pixmap

    monkeypatch.setattr(fitz.Page, "get_pixmap", tracking_get_pixmap)
    # Pretend only tiny images are accepted, forcing every lower DPI to be tried.
    monkeypatch.setattr(pdf_service, "MAX_IMAGE_BYTES", 1)

    document = fitz.open(stream=make_scanned_pdf(), filetype="pdf")
    image = pdf_service._render_page(document[0])
    document.close()

    assert sizes == list(pdf_service.RENDER_DPIS)
    assert image.startswith(b"\xff\xd8")  # still a JPEG


def test_ocr_refuses_to_run_without_a_key(monkeypatch):
    monkeypatch.setattr(settings, "OCR_SPACE_API_KEY", "")

    with pytest.raises(DocumentError, match="may be scanned"):
        ocr_service.ocr_pages([b"jpeg"])


def test_ocr_client_uses_the_configured_timeout(monkeypatch):
    monkeypatch.setattr(settings, "OCR_TIMEOUT_SECONDS", 12.0)

    with ocr_service._client() as client:
        assert client.timeout.read == 12.0
