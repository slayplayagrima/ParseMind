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
from workflows.parallel import run_parallel

logger = logging.getLogger(__name__)


def run(document_text: str) -> WorkflowResponse:
    """
    Analyze a contract using multiple AI skills.
    """

    logger.info("Executing Contract Workflow.")

    start = time.perf_counter()

    results = run_parallel(
        {
            "summary": lambda: summarize(document_text),
            "contract": lambda: parse_contract(document_text),
            "entities": lambda: extract_entities(document_text),
            "clauses": lambda: extract_clauses(document_text),
            "risks": lambda: detect_risks(document_text),
        }
    )

    summary = results["summary"]

    contract_response = results["contract"]

    entities_response = results["entities"]

    clauses_response = results["clauses"]

    risks_response = results["risks"]

    contract: ContractResponse = contract_response.result

    contract.summary = summary.result

    contract.important_clauses = clauses_response.result

    contract.risks = risks_response.result

    contract.recommendations = [risk.recommendation for risk in risks_response.result]

    execution_time = int((time.perf_counter() - start) * 1000)

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
