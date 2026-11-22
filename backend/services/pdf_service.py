import logging

import fitz

from config.settings import settings
from services.errors import DocumentError
from services.ocr_service import MAX_IMAGE_BYTES, ocr_enabled, ocr_pages
from services.text_cleaning import clean_text

logger = logging.getLogger(__name__)


def _validate_pdf(pdf_bytes: bytes) -> None:
    """
    Validate the uploaded PDF before processing.
    """

    if not pdf_bytes:
        raise DocumentError("Uploaded PDF is empty.")


# Tried in order until a page fits under the OCR upload limit.
RENDER_DPIS = (200, 150, 100, 72)


def _render_page(page: fitz.Page) -> bytes:
    """
    Render a page to a JPEG small enough for the OCR service.
    """

    image = b""

    for dpi in RENDER_DPIS:
        image = page.get_pixmap(dpi=dpi).tobytes("jpeg", jpg_quality=80)
        if len(image) <= MAX_IMAGE_BYTES:
            break

    return image


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from a PDF document.

    Args:
        pdf_bytes: Raw PDF file bytes.

    Returns:
        Cleaned text extracted from all pages.

    Raises:
        DocumentError: If the PDF is empty, invalid, encrypted,
                       too long, or contains no extractable text.

    Scanned PDFs have no text layer. When OCR is configured, their pages
    are rendered to images and read by OCR instead.
    """

    _validate_pdf(pdf_bytes)

    try:
        document = fitz.open(stream=pdf_bytes, filetype="pdf")

    except Exception as e:
        logger.exception("Failed to open PDF.")
        raise DocumentError("Invalid or corrupted PDF file.") from e

    try:
        if document.needs_pass:
            raise DocumentError("Password-protected PDFs are not supported.")

        if document.page_count > settings.MAX_PDF_PAGES:
            raise DocumentError(
                f"PDF has {document.page_count} pages. The limit is {settings.MAX_PDF_PAGES} pages."
            )

        extracted_pages = []

        for page in document:
            page_text = page.get_text("text", sort=True)

            if page_text:
                extracted_pages.append(page_text)

        page_images: list[bytes] = []

        if not clean_text("\n".join(extracted_pages)) and ocr_enabled():
            if document.page_count > settings.OCR_MAX_PAGES:
                raise DocumentError(
                    f"Scanned PDFs can have up to {settings.OCR_MAX_PAGES} pages. "
                    f"This one has {document.page_count}."
                )

            page_images = [_render_page(page) for page in document]

    finally:
        document.close()

    if page_images:
        cleaned_text = clean_text(ocr_pages(page_images))
        logger.info("Read %d characters with OCR.", len(cleaned_text))
    else:
        cleaned_text = clean_text("\n".join(extracted_pages))

    if not cleaned_text:
        raise DocumentError(
            "No readable text found in the PDF. The document may be scanned or image-only."
        )

    logger.info(
        "Successfully extracted %d characters.",
        len(cleaned_text),
    )

    return cleaned_text


__all__ = [
    "extract_text_from_pdf",
]
