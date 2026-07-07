from typing import Any

from pydantic import BaseModel


class WorkflowMetadata(BaseModel):
    workflow: str

    success: bool

    model: str

    confidence: float

    execution_time_ms: int


class WorkflowResponse(BaseModel):
    metadata: WorkflowMetadata

    result: Any