from pydantic import BaseModel

from schemas.contract import ContractResponse
from schemas.entities import EntityResponse


class ContractWorkflowResult(BaseModel):
    contract: ContractResponse
    entities: EntityResponse