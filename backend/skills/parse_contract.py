import logging
import time

from schemas.contract import ContractResponse
from schemas.skill import SkillMetadata, SkillResponse
from services.llm_client import generate_json_response
from prompts.contract import CONTRACT_PARSE_PROMPT

logger = logging.getLogger(__name__)

CONTRACT_PARSE_PROMPT = """
You are an expert legal contract parser.

Extract factual information from the contract.

Return ONLY valid JSON.

Use EXACTLY this schema:

{
  "contract_type": "",
  "title": "",

  "parties": [
    {
      "name": "",
      "role": ""
    }
  ],

  "effective_date": null,

  "termination_date": null,

  "duration": null,

  "governing_law": null,

  "jurisdiction": null,

  "payment_terms": {
    "amount": null,
    "currency": null,
    "due_date": null,
    "frequency": null
  },

  "obligations": []
}

Rules:

- Extract factual information only.
- Do not summarize.
- Do not analyze risks.
- Do not extract clauses.
- Do not invent information.
- Return JSON only.
"""


def parse_contract(
    document_text: str,
) -> SkillResponse[ContractResponse]:
    """
    Parse a contract into structured factual information.
    """

    logger.info("Parsing contract.")

    start = time.perf_counter()

    prompt = f"""
{CONTRACT_PARSE_PROMPT}

Contract:

{document_text}
"""

    response = generate_json_response(prompt)

    contract = ContractResponse.model_validate(
        {
            **response,
            "summary": "",
            "important_clauses": [],
            "risks": [],
            "recommendations": [],
        }
    )

    elapsed = int((time.perf_counter() - start) * 1000)

    metadata = SkillMetadata(
        skill="parse_contract",
        success=True,
        execution_time_ms=elapsed,
    )

    return SkillResponse(
        metadata=metadata,
        result=contract,
    )