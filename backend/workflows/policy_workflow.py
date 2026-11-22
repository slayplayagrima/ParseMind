import logging
import time

from schemas.policy import PolicyResponse
from schemas.policy_workflow import PolicyWorkflowResult
from schemas.workflow import WorkflowMetadata, WorkflowResponse
from services.llm_client import DEFAULT_MODEL
from skills.extract_entities import extract_entities
from skills.parse_policy import parse_policy
from skills.summarize import summarize
from workflows.parallel import run_parallel

logger = logging.getLogger(__name__)


def run(document_text: str) -> WorkflowResponse:
    """
    Analyze a policy using multiple AI skills.
    """

    logger.info("Executing Policy Workflow.")

    start = time.perf_counter()

    results = run_parallel(
        {
            "summary": lambda: summarize(document_text),
            "policy": lambda: parse_policy(document_text),
            "entities": lambda: extract_entities(document_text),
        }
    )

    policy: PolicyResponse = results["policy"].result

    policy.summary = results["summary"].result

    execution_time = int((time.perf_counter() - start) * 1000)

    metadata = WorkflowMetadata(
        workflow="policy_workflow",
        success=True,
        model=DEFAULT_MODEL,
        confidence=0.95,
        execution_time_ms=execution_time,
    )

    logger.info(
        "Policy Workflow completed in %d ms.",
        execution_time,
    )

    return WorkflowResponse(
        metadata=metadata,
        result=PolicyWorkflowResult(
            policy=policy,
            entities=results["entities"].result,
        ),
    )
