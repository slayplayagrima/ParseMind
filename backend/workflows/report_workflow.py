import logging
import time

from schemas.report import ReportResponse
from schemas.report_workflow import ReportWorkflowResult
from schemas.workflow import WorkflowMetadata, WorkflowResponse
from services.llm_client import DEFAULT_MODEL
from skills.extract_entities import extract_entities
from skills.parse_report import parse_report
from skills.summarize import summarize
from workflows.parallel import run_parallel

logger = logging.getLogger(__name__)


def run(document_text: str) -> WorkflowResponse:
    """
    Analyze a report using multiple AI skills.
    """

    logger.info("Executing Report Workflow.")

    start = time.perf_counter()

    results = run_parallel(
        {
            "summary": lambda: summarize(document_text),
            "report": lambda: parse_report(document_text),
            "entities": lambda: extract_entities(document_text),
        }
    )

    report: ReportResponse = results["report"].result

    report.summary = results["summary"].result

    execution_time = int((time.perf_counter() - start) * 1000)

    metadata = WorkflowMetadata(
        workflow="report_workflow",
        success=True,
        model=DEFAULT_MODEL,
        confidence=0.95,
        execution_time_ms=execution_time,
    )

    logger.info(
        "Report Workflow completed in %d ms.",
        execution_time,
    )

    return WorkflowResponse(
        metadata=metadata,
        result=ReportWorkflowResult(
            report=report,
            entities=results["entities"].result,
        ),
    )
