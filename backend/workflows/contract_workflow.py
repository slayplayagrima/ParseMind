import logging
import time

from schemas.contract import ContractResponse
from schemas.contract_workflow import ContractWorkflowResult
from schemas.workflow import WorkflowMetadata, WorkflowResponse
from services.llm_client import DEFAULT_MODEL

from skills.clause_extractor import extract_clauses
from skills.extract_entities import extract_entities
from skills.parse_contract import parse_contract
from skills.risk_detector import detect_risks
from skills.summarize import summarize

logger = logging.getLogger(__name__)


def run(document_text: str) -> WorkflowResponse:
    """
    Analyze a contract using multiple AI skills.
    """

    logger.info("Executing Contract Workflow.")

    start = time.perf_counter()

    summary = summarize(document_text)

    contract_response = parse_contract(document_text)

    entities_response = extract_entities(document_text)

    clauses_response = extract_clauses(document_text)

    risks_response = detect_risks(document_text)

    contract: ContractResponse = contract_response.result

    contract.summary = summary.result

    contract.important_clauses = clauses_response.result

    contract.risks = risks_response.result

    contract.recommendations = [
        risk.recommendation
        for risk in risks_response.result
    ]

    execution_time = int(
        (time.perf_counter() - start) * 1000
    )

    metadata = WorkflowMetadata(
        workflow="contract_workflow",
        success=True,
        model=DEFAULT_MODEL,
        confidence=0.95,
        execution_time_ms=execution_time,
    )

    logger.info(
        "Contract Workflow completed in %d ms.",
        execution_time,
    )

    return WorkflowResponse(
        metadata=metadata,
        result=ContractWorkflowResult(
            contract=contract,
            entities=entities_response.result,
        ),
    )