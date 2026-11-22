import zipfile
from io import BytesIO
from types import SimpleNamespace

import pytest

from config.settings import settings
from services import document_processor
from services.docx_service import extract_text_from_docx
from services.errors import DocumentError
from services.file_types import DOCX_MIME, FileType, detect_file_type
from services.text_cleaning import clean_text
from services.txt_service import extract_text_from_txt

NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def paragraph(text: str) -> str:
    return f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>"


def make_docx(body: str, *, part: str = "word/document.xml") -> bytes:
    """
    Build a minimal .docx in memory. Word only needs document.xml for text.
    """

    buffer = BytesIO()

    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr(part, f"<w:document {NS}><w:body>{body}</w:body></w:document>")

    return buffer.getvalue()


# Text cleaning


def test_clean_text_normalizes_whitespace():
    assert clean_text("a\r\nb\t\t c\n\n\n\nd  ") == "a\nb c\n\nd"


# DOCX


def test_docx_paragraphs_are_read_in_order():
    data = make_docx(paragraph("Service Agreement") + paragraph("Between Acme and Beta."))

    assert extract_text_from_docx(data) == "Service Agreement\nBetween Acme and Beta."


def test_docx_runs_tabs_and_breaks_are_kept():
    body = (
        "<w:p><w:r><w:t>Name:</w:t><w:tab/><w:t>Jane</w:t></w:r>"
        "<w:r><w:br/><w:t xml:space='preserve'>Doe</w:t></w:r></w:p>"
    )

    assert extract_text_from_docx(make_docx(body)) == "Name: Jane\nDoe"


def row(*cells: str) -> str:
    return "<w:tr>" + "".join(f"<w:tc>{paragraph(c)}</w:tc>" for c in cells) + "</w:tr>"


def test_docx_tables_become_rows():
    table = "<w:tbl>" + row("Item", "Amount") + row("Design", "500") + "</w:tbl>"

    text = extract_text_from_docx(make_docx(paragraph("Invoice INV-1") + table))

    assert text == "Invoice INV-1\nItem | Amount\nDesign | 500"


def test_docx_content_controls_are_read():
    body = "<w:sdt><w:sdtContent>" + paragraph("Inside a form field") + "</w:sdtContent></w:sdt>"

    assert extract_text_from_docx(make_docx(body)) == "Inside a form field"


@pytest.mark.parametrize(
    ("data", "message"),
    [
        (b"", "empty"),
        (b"not a zip at all", "not a valid Word document"),
        (make_docx(paragraph("x"), part="other.xml"), "not a valid Word document"),
        (make_docx("<w:p>"), "corrupted"),
        (make_docx(""), "No readable text"),
    ],
)
def test_docx_bad_files_raise_document_error(data, message):
    with pytest.raises(DocumentError, match=message):
        extract_text_from_docx(data)


def test_docx_length_limit(monkeypatch):
    monkeypatch.setattr(settings, "MAX_DOCUMENT_CHARS", 10)

    with pytest.raises(DocumentError, match="10 characters"):
        extract_text_from_docx(make_docx(paragraph("This is far too long.")))


def test_docx_refuses_oversized_xml(monkeypatch):
    from services import docx_service

    monkeypatch.setattr(docx_service, "MAX_XML_BYTES", 100)

    with pytest.raises(DocumentError, match="too large"):
        extract_text_from_docx(make_docx(paragraph("x" * 200)))


# TXT


def test_txt_is_decoded_and_cleaned():
    data = "﻿Invoice INV-7\r\n\r\n\r\n\r\nTotal:\t$99".encode()

    assert extract_text_from_txt(data) == "Invoice INV-7\n\nTotal: $99"


@pytest.mark.parametrize(
    ("data", "message"),
    [
        (b"", "empty"),
        (b"   \n\t ", "empty"),
        ("café".encode("latin-1"), "UTF-8"),
        (b"abc\x00def", "not a text file"),
    ],
)
def test_txt_bad_files_raise_document_error(data, message):
    with pytest.raises(DocumentError, match=message):
        extract_text_from_txt(data)


def test_txt_length_limit(monkeypatch):
    monkeypatch.setattr(settings, "MAX_DOCUMENT_CHARS", 5)

    with pytest.raises(DocumentError, match="too long"):
        extract_text_from_txt(b"123456")


# File type detection


@pytest.mark.parametrize(
    ("data", "name", "mime", "expected"),
    [
        (b"%PDF-1.7", "contract.pdf", "application/pdf", FileType.PDF),
        # Bytes win: a real PDF with a wrong name or type is still a PDF.
        (b"%PDF-1.7", "download", "application/octet-stream", FileType.PDF),
        (b"PK\x03\x04", "cv.docx", DOCX_MIME, FileType.DOCX),
        (b"PK\x03\x04", "cv.docx", "application/octet-stream", FileType.DOCX),
        (b"hello", "notes.txt", "text/plain", FileType.TXT),
        (b"hello", "notes.txt", "text/plain; charset=utf-8", FileType.TXT),
        (b"hello", "NOTES.TXT", None, FileType.TXT),
    ],
)
def test_detects_supported_types(data, name, mime, expected):
    assert detect_file_type(data, name, mime) == expected


@pytest.mark.parametrize(
    ("data", "name", "mime", "message"),
    [
        (b"hello", "fake.pdf", "application/pdf", "not a valid PDF"),
        (b"hello", "fake.docx", DOCX_MIME, "not a valid Word document"),
        (b"\xd0\xcf\x11\xe0", "old.doc", "application/msword", "Older .doc files"),
        (b"\x89PNG", "scan.png", "image/png", "Only PDF, Word"),
        (b"", None, None, "Only PDF, Word"),
    ],
)
def test_rejects_unsupported_or_mislabelled_files(data, name, mime, message):
    with pytest.raises(DocumentError, match=message):
        detect_file_type(data, name, mime)


# Pipeline


def test_pipeline_uses_the_reader_for_the_file_type(monkeypatch):
    seen = {}

    monkeypatch.setattr(
        document_processor, "classify_document", lambda _: SimpleNamespace(workflow="fake")
    )

    def fake_dispatch(router_response, text):
        seen["text"] = text
        return "done"

    monkeypatch.setattr(document_processor, "dispatch_workflow", fake_dispatch)

    data = make_docx(paragraph("Resume of Jane Doe"))

    assert document_processor.process_document(data, FileType.DOCX) == "done"
    assert seen["text"] == "Resume of Jane Doe"

    assert document_processor.process_document(b"Plain resume", FileType.TXT) == "done"
    assert seen["text"] == "Plain resume"
