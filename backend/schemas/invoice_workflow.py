from pydantic import BaseModel

from schemas.entities import EntityResponse
from schemas.invoice import InvoiceResponse


class InvoiceWorkflowResult(BaseModel):
    invoice: InvoiceResponse
    entities: EntityResponse
