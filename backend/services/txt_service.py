import logging

from config.settings import settings
from services.errors import DocumentError
from services.text_cleaning import clean_text

logger = logging.getLogger(__name__)


def extract_text_from_txt(txt_bytes: bytes) -> str:
    """
    Decode a plain text upload.

    Raises:
        DocumentError: If the file is empty, not UTF-8 text, or too long.
    """

    if not txt_bytes:
        raise DocumentError("Uploaded document is empty.")

    try:
        # utf-8-sig also strips the byte order mark Windows editors add.
        text = txt_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as e:
        raise DocumentError("The text file must be UTF-8 encoded.") from e

    if "\x00" in text:
        raise DocumentError("The uploaded file is not a text file.")

    text = clean_text(text)

    if not text:
        raise DocumentError("The text file is empty.")

    if len(text) > settings.MAX_DOCUMENT_CHARS:
        raise DocumentError(
            f"The document is too long. The limit is {settings.MAX_DOCUMENT_CHARS:,} characters."
        )

    logger.info("Read %d characters from TXT.", len(text))

    return text


__all__ = [
    "extract_text_from_txt",
]
