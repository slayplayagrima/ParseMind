import logging
import time

from prompts.report import REPORT_PARSE_PROMPT
from schemas.report import ReportResponse
from schemas.skill import SkillMetadata, SkillResponse
from services.llm_client import generate_json_response

logger = logging.getLogger(__name__)


def parse_report(document_text: str) -> SkillResponse[ReportResponse]:
    """
    Parse a report into structured data.
    """

    logger.info("Parsing report.")

    start = time.perf_counter()

    prompt = f"""
{REPORT_PARSE_PROMPT}

Report:

{document_text}
"""

    response = generate_json_response(prompt)

    # The summary comes from the summarize skill, not this one.
    response.pop("summary", None)

    report = ReportResponse.model_validate(response)

    elapsed = int((time.perf_counter() - start) * 1000)

    metadata = SkillMetadata(
        skill="parse_report",
        success=True,
        execution_time_ms=elapsed,
    )

    return SkillResponse(
        metadata=metadata,
        result=report,
    )
