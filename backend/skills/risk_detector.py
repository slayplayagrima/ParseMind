import logging
import time

from schemas.contract import Risk
from schemas.skill import SkillMetadata, SkillResponse
from services.llm_client import generate_json_response
from prompts.risks import RISK_DETECTION_PROMPT

logger = logging.getLogger(__name__)


def detect_risks(
    document_text: str,
) -> SkillResponse[list[Risk]]:
    """
    Analyze a contract for legal and business risks.
    """

    logger.info("Detecting contract risks.")

    start = time.perf_counter()

    prompt = f"""
{RISK_DETECTION_PROMPT}

Contract:

{document_text}
"""

    response = generate_json_response(prompt)

    risks = [
        Risk.model_validate(item)
        for item in response["risks"]
    ]

    elapsed = int((time.perf_counter() - start) * 1000)

    metadata = SkillMetadata(
        skill="detect_risks",
        success=True,
        execution_time_ms=elapsed,
    )

    return SkillResponse(
        metadata=metadata,
        result=risks,
    )