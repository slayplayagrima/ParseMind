import logging

from schemas.router import RouterResponse
from services.errors import DocumentError
from workflows import (
    contract_workflow,
    invoice_workflow,
    resume_workflow,
)

logger = logging.getLogger(__name__)

WORKFLOWS = {
    "resume_workflow": resume_workflow.run,
    "contract_workflow": contract_workflow.run,
    "invoice_workflow": invoice_workflow.run,
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
            "This document type is not supported yet. Try a contract, a resume or an invoice."
        )

    workflow = WORKFLOWS.get(router_response.workflow)

    if workflow is None:
        # The router can recognise types (reports, policies) that have no workflow yet.
        logger.warning("No workflow registered for '%s'.", router_response.workflow)
        raise DocumentError(
            f"{router_response.document_type.title()} documents are not supported yet. "
            "Try a contract, a resume or an invoice."
        )

    logger.info(
        "Dispatching to '%s'.",
        router_response.workflow,
    )

    return workflow(document_text)
