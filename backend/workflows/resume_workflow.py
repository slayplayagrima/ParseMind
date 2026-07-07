import logging
import time

from schemas.resume import ResumeResponse
from schemas.resume_workflow import ResumeWorkflowResult
from schemas.workflow import WorkflowMetadata, WorkflowResponse
from services.llm_client import DEFAULT_MODEL

from skills.extract_entities import extract_entities
from skills.parse_resume import parse_resume
from skills.summarize import summarize

logger = logging.getLogger(__name__)


def run(document_text: str) -> WorkflowResponse:
    """
    Analyze a resume using multiple AI skills.
    """

    logger.info("Executing Resume Workflow.")

    start = time.perf_counter()

    summary = summarize(document_text)

    resume_response = parse_resume(document_text)

    entities_response = extract_entities(document_text)

    resume: ResumeResponse = resume_response.result

    resume.summary = summary.result

    execution_time = int(
        (time.perf_counter() - start) * 1000
    )

    metadata = WorkflowMetadata(
        workflow="resume_workflow",
        success=True,
        model=DEFAULT_MODEL,
        confidence=0.95,
        execution_time_ms=execution_time,
    )

    logger.info(
        "Resume Workflow completed in %d ms.",
        execution_time,
    )

    return WorkflowResponse(
        metadata=metadata,
        result=ResumeWorkflowResult(
            resume=resume,
            entities=entities_response.result,
        ),
    )