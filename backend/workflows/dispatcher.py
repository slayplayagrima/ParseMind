import logging

from schemas.router import RouterResponse
from services.errors import DocumentError
from workflows import (
    contract_workflow,
    resume_workflow,
)

logger = logging.getLogger(__name__)

WORKFLOWS = {
    "resume_workflow": resume_workflow.run,
    "contract_workflow": contract_workflow.run,
}


def dispatch_workflow(
    router_response: RouterResponse,
    document_text: str,
):
    """
    Dispatch the document to the appropriate workflow.
    """

    if not router_response.supported:
        raise DocumentError("This document type is not supported yet. Try a contract or a resume.")

    workflow = WORKFLOWS.get(router_response.workflow)

    if workflow is None:
        raise ValueError(f"Workflow '{router_response.workflow}' not found.")

    logger.info(
        "Dispatching to '%s'.",
        router_response.workflow,
    )

    return workflow(document_text)
