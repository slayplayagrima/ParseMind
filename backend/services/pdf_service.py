import logging

import fitz

from config.settings import settings
from services.errors import DocumentError
from services.text_cleaning import clean_text

logger = logging.getLogger(__name__)


def _validate_pdf(pdf_bytes: bytes) -> None:
    """
    Validate the uploaded PDF before processing.
    """

    if not pdf_bytes:
        raise DocumentError("Uploaded PDF is empty.")


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

    finally:
        document.close()

    full_text = "\n".join(extracted_pages)

    cleaned_text = clean_text(full_text)

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
