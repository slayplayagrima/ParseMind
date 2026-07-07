from pydantic import BaseModel

from schemas.entities import EntityResponse
from schemas.resume import ResumeResponse


class ResumeWorkflowResult(BaseModel):
    resume: ResumeResponse
    entities: EntityResponse