import logging
import time

from prompts.entities import ENTITY_EXTRACTION_PROMPT
from schemas.entities import EntityResponse
from schemas.skill import SkillMetadata, SkillResponse
from services.llm_client import generate_json_response

logger = logging.getLogger(__name__)


def extract_entities(
    document_text: str,
) -> SkillResponse[EntityResponse]:
    """
    Extract named entities from a document.
    """

    logger.info("Extracting entities.")

    start = time.perf_counter()

    prompt = f"""
{ENTITY_EXTRACTION_PROMPT}

Document:

{document_text}
"""

    entities = EntityResponse.model_validate(
        generate_json_response(prompt)
    )

    elapsed = int((time.perf_counter() - start) * 1000)

    metadata = SkillMetadata(
        skill="extract_entities",
        success=True,
        execution_time_ms=elapsed,
    )

    return SkillResponse(
        metadata=metadata,
        result=entities,
    )