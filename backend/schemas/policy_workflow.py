from pydantic import BaseModel

from schemas.entities import EntityResponse
from schemas.policy import PolicyResponse


class PolicyWorkflowResult(BaseModel):
    policy: PolicyResponse
    entities: EntityResponse
