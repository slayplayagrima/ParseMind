import logging
import re

import fitz
logger = logging.getLogger(__name__)

def _validate_pdf(pdf_bytes: bytes) -> None:
    """
    Validate the uploaded PDF before processing.
    """

    if not pdf_bytes:
        raise ValueError("Uploaded PDF is empty.")

def _clean_text(text: str) -> str:
    """
    Normalize extracted text.
    """

    text = re.sub(r"\r\n?", "\n", text)

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from a PDF document.

    Args:
        pdf_bytes: Raw PDF file bytes.

    Returns:
        Cleaned text extracted from all pages.

    Raises:
        ValueError: If the PDF is empty, invalid, encrypted,
                    or contains no extractable text.
    """

    _validate_pdf(pdf_bytes)

    try:
        document = fitz.open(stream=pdf_bytes, filetype="pdf")

    except Exception as e:
        logger.exception("Failed to open PDF.")
        raise ValueError("Invalid or corrupted PDF file.") from e

    try:

        if document.needs_pass:
            raise ValueError("Password-protected PDFs are not supported.")

        extracted_pages = []

        for page in document:

            page_text = page.get_text("text", sort=True)

            if page_text:
                extracted_pages.append(page_text)

        document.close()

        full_text = "\n".join(extracted_pages)

        cleaned_text = _clean_text(full_text)

        if not cleaned_text:
            raise ValueError(
                "No readable text found in the PDF. "
                "The document may be scanned or image-only."
            )

        logger.info(
            "Successfully extracted %d characters.",
            len(cleaned_text),
        )

        return cleaned_text

    except Exception:

        document.close()

        raise
__all__ = [
    "extract_text_from_pdf",
]