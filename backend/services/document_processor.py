from agents.router_agent import classify_document
from services.pdf_service import extract_text_from_pdf
from workflows.dispatcher import dispatch_workflow

import logging

logger = logging.getLogger(__name__)


def process_document(
    pdf_bytes: bytes,
):
    """
    Complete document processing pipeline.
    """

    logger.info("Starting document processing.")

    document_text = extract_text_from_pdf(pdf_bytes)

    logger.info(
        "Extracted %d characters from PDF.",
        len(document_text),
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