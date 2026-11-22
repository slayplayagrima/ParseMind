import logging
import time

from schemas.invoice import InvoiceResponse
from schemas.invoice_workflow import InvoiceWorkflowResult
from schemas.workflow import WorkflowMetadata, WorkflowResponse
from services.llm_client import DEFAULT_MODEL
from skills.extract_entities import extract_entities
from skills.parse_invoice import parse_invoice
from skills.summarize import summarize
from skills.validate_invoice import validate_invoice
from workflows.parallel import run_parallel

logger = logging.getLogger(__name__)


def run(document_text: str) -> WorkflowResponse:
    """
    Analyze an invoice using multiple AI skills, then check its totals.
    """

    logger.info("Executing Invoice Workflow.")

    start = time.perf_counter()

    results = run_parallel(
        {
            "summary": lambda: summarize(document_text),
            "invoice": lambda: parse_invoice(document_text),
            "entities": lambda: extract_entities(document_text),
        }
    )

    invoice: InvoiceResponse = results["invoice"].result

    invoice.summary = results["summary"].result

    invoice.issues = validate_invoice(invoice)

    execution_time = int((time.perf_counter() - start) * 1000)

    metadata = WorkflowMetadata(
        workflow="invoice_workflow",
        success=True,
        model=DEFAULT_MODEL,
        confidence=0.95,
        execution_time_ms=execution_time,
    )

    logger.info(
        "Invoice Workflow completed in %d ms with %d issue(s).",
        execution_time,
        len(invoice.issues),
    )

    return WorkflowResponse(
        metadata=metadata,
        result=InvoiceWorkflowResult(
            invoice=invoice,
            entities=results["entities"].result,
        ),
    )
