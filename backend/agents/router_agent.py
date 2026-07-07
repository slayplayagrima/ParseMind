from urllib import response
from prompts.router import ROUTER_PROMPT
from schemas import router
from schemas.router import RouterResponse
from services.llm_client import generate_json_response

import logging

logger = logging.getLogger(__name__)

def classify_document(
    document_text: str,
) -> RouterResponse:
    """
    Classify an uploaded document.
    """

    logger.info("Classifying uploaded document.")

    prompt = f"""
{ROUTER_PROMPT}

Document:

{document_text[:12000]}
"""

    response = generate_json_response(prompt)

    router = RouterResponse.model_validate(response)

    logger.info(
    "Document classified as '%s' (workflow=%s, confidence=%.2f)",
    router.document_type,
    router.workflow,
    router.confidence,
    )

    return router