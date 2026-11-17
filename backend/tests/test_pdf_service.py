from pathlib import Path

import pytest

from config.settings import settings
from services.errors import DocumentError
from services.pdf_service import extract_text_from_pdf
from tests.conftest import make_pdf


def test_extracts_text():
    text = extract_text_from_pdf(make_pdf(text="Payment is due within 30 days."))

    assert "Payment is due within 30 days." in text


def test_extracts_sample_pdf():
    sample = Path(__file__).parent / "sample.pdf"

    assert extract_text_from_pdf(sample.read_bytes())


def test_empty_upload_is_rejected():
    with pytest.raises(DocumentError, match="empty"):
        extract_text_from_pdf(b"")


def test_corrupted_pdf_is_rejected():
    with pytest.raises(DocumentError, match="Invalid or corrupted"):
        extract_text_from_pdf(b"%PDF-1.7 garbage")


def test_page_limit(monkeypatch):
    monkeypatch.setattr(settings, "MAX_PDF_PAGES", 2)

    with pytest.raises(DocumentError, match="3 pages"):
        extract_text_from_pdf(make_pdf(pages=3))


def test_pdf_without_text_is_rejected():
    with pytest.raises(DocumentError, match="No readable text"):
        extract_text_from_pdf(make_pdf(text=""))
