import logging
from collections.abc import Callable

from agents.router_agent import classify_document
from services.docx_service import extract_text_from_docx
from services.file_types import FileType
from services.pdf_service import extract_text_from_pdf
from services.txt_service import extract_text_from_txt
from workflows.dispatcher import dispatch_workflow

logger = logging.getLogger(__name__)

EXTRACTORS: dict[FileType, Callable[[bytes], str]] = {
    FileType.PDF: extract_text_from_pdf,
    FileType.DOCX: extract_text_from_docx,
    FileType.TXT: extract_text_from_txt,
}


def extract_text(data: bytes, file_type: FileType) -> str:
    return EXTRACTORS[file_type](data)


def process_document(
    data: bytes,
    file_type: FileType = FileType.PDF,
):
    """
    Complete document processing pipeline.
    """

    logger.info("Starting document processing (%s).", file_type)

    document_text = extract_text(data, file_type)

    logger.info(
        "Extracted %d characters from %s.",
        len(document_text),
        file_type.upper(),
    )

    router_response = classify_document(document_text)

    logger.info(
        "Selected workflow: %s",
        router_response.workflow,
    )

    result = dispatch_workflow(
        router_response,
        document_text,
    )

    logger.info("Document processing completed.")

    return result
