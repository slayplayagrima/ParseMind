import logging
import time

from schemas.contract import Clause
from schemas.skill import SkillMetadata, SkillResponse
from services.llm_client import generate_json_response
from prompts.clauses import CLAUSE_EXTRACTION_PROMPT

logger = logging.getLogger(__name__)

def extract_clauses(
    document_text: str,
) -> SkillResponse[list[Clause]]:
    """
    Extract important clauses from a contract.
    """

    logger.info("Extracting contract clauses.")

    start = time.perf_counter()

    prompt = f"""
{CLAUSE_EXTRACTION_PROMPT}

Contract:

{document_text}
"""

    response = generate_json_response(prompt)

    clauses = [
        Clause.model_validate(item)
        for item in response["clauses"]
    ]

    elapsed = int((time.perf_counter() - start) * 1000)

    metadata = SkillMetadata(
        skill="extract_clauses",
        success=True,
        execution_time_ms=elapsed,
    )

    return SkillResponse(
        metadata=metadata,
        result=clauses,
    )