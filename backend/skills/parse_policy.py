import logging
import time

from prompts.policy import POLICY_PARSE_PROMPT
from schemas.policy import PolicyResponse
from schemas.skill import SkillMetadata, SkillResponse
from services.llm_client import generate_json_response

logger = logging.getLogger(__name__)


def parse_policy(document_text: str) -> SkillResponse[PolicyResponse]:
    """
    Parse a policy into structured rules and compliance gaps.
    """

    logger.info("Parsing policy.")

    start = time.perf_counter()

    prompt = f"""
{POLICY_PARSE_PROMPT}

Policy:

{document_text}
"""

    response = generate_json_response(prompt)

    # The summary comes from the summarize skill, not this one.
    response.pop("summary", None)

    policy = PolicyResponse.model_validate(response)

    elapsed = int((time.perf_counter() - start) * 1000)

    metadata = SkillMetadata(
        skill="parse_policy",
        success=True,
        execution_time_ms=elapsed,
    )

    return SkillResponse(
        metadata=metadata,
        result=policy,
    )
