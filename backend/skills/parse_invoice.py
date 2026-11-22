import logging
import time

from prompts.invoice import INVOICE_PARSE_PROMPT
from schemas.invoice import InvoiceResponse
from schemas.skill import SkillMetadata, SkillResponse
from services.llm_client import generate_json_response

logger = logging.getLogger(__name__)


def parse_invoice(document_text: str) -> SkillResponse[InvoiceResponse]:
    """
    Parse an invoice into structured data.
    """

    logger.info("Parsing invoice.")

    start = time.perf_counter()

    prompt = f"""
{INVOICE_PARSE_PROMPT}

Invoice:

{document_text}
"""

    response = generate_json_response(prompt)

    # The model must not fill these; the workflow does.
    response.pop("summary", None)
    response.pop("issues", None)

    invoice = InvoiceResponse.model_validate(response)

    elapsed = int((time.perf_counter() - start) * 1000)

    metadata = SkillMetadata(
        skill="parse_invoice",
        success=True,
        execution_time_ms=elapsed,
    )

    return SkillResponse(
        metadata=metadata,
        result=invoice,
    )
