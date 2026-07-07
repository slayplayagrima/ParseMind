import logging
import time
from prompts.summarize import SUMMARY_PROMPT
from schemas.skill import SkillMetadata, SkillResponse
from services.llm_client import generate_text_response

logger = logging.getLogger(__name__)


def summarize(document_text: str) -> SkillResponse[str]:
    """
    Generate a concise summary of a document.
    """

    logger.info("Generating document summary.")

    start = time.perf_counter()

    prompt = f"""
{SUMMARY_PROMPT}

Document:

{document_text}
"""

    summary = generate_text_response(prompt)

    elapsed = int((time.perf_counter() - start) * 1000)

    metadata = SkillMetadata(
        skill="summarize",
        success=True,
        execution_time_ms=elapsed,
    )

    return SkillResponse(
        metadata=metadata,
        result=summary,
    )