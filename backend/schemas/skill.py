from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class SkillMetadata(BaseModel):
    skill: str
    success: bool
    execution_time_ms: int

class SkillResponse(BaseModel, Generic[T]):
    metadata: SkillMetadata
    result: T