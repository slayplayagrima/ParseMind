import logging
import zipfile
from io import BytesIO
from xml.etree import ElementTree

from config.settings import settings
from services.errors import DocumentError
from services.text_cleaning import clean_text

logger = logging.getLogger(__name__)

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

DOCUMENT_PART = "word/document.xml"

# A real document.xml is a few MB at most. Refuse anything that would
# inflate far beyond that, so a zip bomb can't exhaust memory.
MAX_XML_BYTES = 50 * 1024 * 1024


def _paragraph_text(paragraph: ElementTree.Element) -> str:
    parts = []

    for node in paragraph.iter():
        if node.tag == f"{W}t" and node.text:
            parts.append(node.text)
        elif node.tag == f"{W}tab":
            parts.append("\t")
        elif node.tag in (f"{W}br", f"{W}cr"):
            parts.append("\n")

    return "".join(parts)


def _block_lines(element: ElementTree.Element) -> list[str]:
    """
    Walk the body in document order. Tables become one line per row,
    with cells separated by " | " so the model can still read them.
    """

    lines: list[str] = []

    for child in element:
        if child.tag == f"{W}p":
            lines.append(_paragraph_text(child))

        elif child.tag == f"{W}tbl":
            for row in child.iter(f"{W}tr"):
                cells = [
                    " ".join(_paragraph_text(p) for p in cell.iter(f"{W}p")).strip()
                    for cell in row.iter(f"{W}tc")
                ]
                lines.append(" | ".join(cells))

        elif child.tag == f"{W}sdt":
            content = child.find(f"{W}sdtContent")
            if content is not None:
                lines.extend(_block_lines(content))

    return lines


def extract_text_from_docx(docx_bytes: bytes) -> str:
    """
    Extract text from a Word (.docx) document using only the standard library.

    Raises:
        DocumentError: If the file is empty, not a valid .docx, too long,
                       or contains no text.
    """

    if not docx_bytes:
        raise DocumentError("Uploaded document is empty.")

    try:
        with zipfile.ZipFile(BytesIO(docx_bytes)) as archive:
            try:
                info = archive.getinfo(DOCUMENT_PART)
            except KeyError as e:
                raise DocumentError("The uploaded file is not a valid Word document.") from e

            if info.file_size > MAX_XML_BYTES:
                raise DocumentError("The Word document is too large to process.")

            xml = archive.read(info)

    except zipfile.BadZipFile as e:
        raise DocumentError(
            "The uploaded file is not a valid Word document. "
            "Older .doc files are not supported, save it as .docx or PDF."
        ) from e

    try:
        root = ElementTree.fromstring(xml)
    except ElementTree.ParseError as e:
        logger.exception("Failed to parse document.xml.")
        raise DocumentError("The Word document is corrupted.") from e

    body = root.find(f"{W}body")
    lines = _block_lines(body) if body is not None else []

    text = clean_text("\n".join(lines))

    if not text:
        raise DocumentError("No readable text found in the Word document.")

    if len(text) > settings.MAX_DOCUMENT_CHARS:
        raise DocumentError(
            f"The document is too long. The limit is {settings.MAX_DOCUMENT_CHARS:,} characters."
        )

    logger.info("Successfully extracted %d characters from DOCX.", len(text))

    return text


__all__ = [
    "extract_text_from_docx",
]
