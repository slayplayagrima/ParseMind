import logging
import time

from prompts.contract import CONTRACT_PARSE_PROMPT
from schemas.contract import ContractResponse
from schemas.skill import SkillMetadata, SkillResponse
from services.llm_client import generate_json_response

logger = logging.getLogger(__name__)


def parse_contract(
    document_text: str,
) -> SkillResponse[ContractResponse]:
    """
    Parse a contract into structured factual information.
    """

    logger.info("Parsing contract.")

    start = time.perf_counter()

    prompt = f"""
{CONTRACT_PARSE_PROMPT}

Contract:

{document_text}
"""

    response = generate_json_response(prompt)

    contract = ContractResponse.model_validate(
        {
            **response,
            "summary": "",
            "important_clauses": [],
            "risks": [],
            "recommendations": [],
        }
    )

    elapsed = int((time.perf_counter() - start) * 1000)

    metadata = SkillMetadata(
        skill="parse_contract",
        success=True,
        execution_time_ms=elapsed,
    )

    return SkillResponse(
        metadata=metadata,
        result=contract,
    )
