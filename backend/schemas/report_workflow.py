from pydantic import BaseModel

from schemas.entities import EntityResponse
from schemas.report import ReportResponse


class ReportWorkflowResult(BaseModel):
    report: ReportResponse
    entities: EntityResponse
