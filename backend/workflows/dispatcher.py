import logging

from schemas.router import RouterResponse
from services.errors import DocumentError
from workflows import (
    contract_workflow,
    invoice_workflow,
    policy_workflow,
    report_workflow,
    resume_workflow,
)

logger = logging.getLogger(__name__)

WORKFLOWS = {
    "resume_workflow": resume_workflow.run,
    "contract_workflow": contract_workflow.run,
    "invoice_workflow": invoice_workflow.run,
    "report_workflow": report_workflow.run,
    "policy_workflow": policy_workflow.run,
}


def dispatch_workflow(
    router_response: RouterResponse,
    document_text: str,
):
    """
    Dispatch the document to the appropriate workflow.
    """

    if not router_response.supported:
        raise DocumentError(
            "This document type is not supported yet. "
            "Try a contract, resume, invoice, report or policy."
        )

    workflow = WORKFLOWS.get(router_response.workflow)

    if workflow is None:
        # The router may name a workflow that does not exist, or one not built yet.
        logger.warning("No workflow registered for '%s'.", router_response.workflow)
        raise DocumentError(
            f"{router_response.document_type.title()} documents are not supported yet. "
            "Try a contract, resume, invoice, report or policy."
        )

    logger.info(
        "Dispatching to '%s'.",
        router_response.workflow,
    )

    return workflow(document_text)
