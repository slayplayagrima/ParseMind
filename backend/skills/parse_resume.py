import logging

from schemas.resume import ResumeResponse
from schemas.skill import SkillMetadata, SkillResponse
from services.llm_client import generate_json_response
from prompts.resume import RESUME_PARSE_PROMPT
logger = logging.getLogger(__name__)


import time


def parse_resume(document_text: str) -> SkillResponse[ResumeResponse]:
    """
    Parse a resume into structured data.
    """

    logger.info("Parsing resume.")

    start = time.perf_counter()

    prompt = f"""
{RESUME_PARSE_PROMPT}

Resume:

{document_text}
"""

    response = generate_json_response(prompt)

    resume = ResumeResponse.model_validate(
        {
            **response,
            "summary": "",
        }
    )

    elapsed = int((time.perf_counter() - start) * 1000)

    metadata = SkillMetadata(
        skill="parse_resume",
        success=True,
        execution_time_ms=elapsed,
    )

    return SkillResponse(
        metadata=metadata,
        result=resume,
    )