from enum import StrEnum

from services.errors import DocumentError


class FileType(StrEnum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"


DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

UNSUPPORTED_MESSAGE = "Only PDF, Word (.docx) and text (.txt) files are supported."


def detect_file_type(data: bytes, filename: str | None, content_type: str | None) -> FileType:
    """
    Decide how to read an upload. The file's own bytes win over its name
    and the browser's content type, which are easy to get wrong or fake.
    """

    name = (filename or "").lower()
    mime = (content_type or "").split(";")[0].strip().lower()

    if data.startswith(b"%PDF-"):
        return FileType.PDF

    if mime == "application/pdf" or name.endswith(".pdf"):
        raise DocumentError("The uploaded file is not a valid PDF.")

    claims_docx = mime == DOCX_MIME or name.endswith(".docx")

    if claims_docx:
        if data.startswith(b"PK\x03\x04"):
            return FileType.DOCX
        raise DocumentError("The uploaded file is not a valid Word document.")

    if name.endswith(".doc") or mime == "application/msword":
        raise DocumentError("Older .doc files are not supported. Save it as .docx or PDF.")

    if mime == "text/plain" or name.endswith(".txt"):
        return FileType.TXT

    raise DocumentError(UNSUPPORTED_MESSAGE)
