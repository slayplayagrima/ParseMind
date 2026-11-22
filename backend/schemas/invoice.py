import re
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

_NUMBER = re.compile(r"-?\d+(?:\.\d+)?")


def _to_amount(value: object) -> float | None:
    """
    Accept numbers or strings like "$1,250.00" or "1 250,00 EUR" from the model.
    """

    if value is None or isinstance(value, bool):
        return None

    if isinstance(value, int | float):
        return float(value)

    if isinstance(value, str):
        text = value.replace(",", "").replace(" ", "")
        match = _NUMBER.search(text)
        return float(match.group()) if match else None

    return None


Amount = Annotated[float | None, BeforeValidator(_to_amount)]


class InvoiceParty(BaseModel):
    name: str | None = None
    address: str | None = None
    email: str | None = None
    tax_id: str | None = None


class LineItem(BaseModel):
    description: str
    quantity: Amount = None
    unit_price: Amount = None
    amount: Amount = None


class InvoiceResponse(BaseModel):
    invoice_number: str | None = None

    issue_date: str | None = None

    due_date: str | None = None

    currency: str | None = None

    vendor: InvoiceParty = Field(default_factory=InvoiceParty)

    customer: InvoiceParty = Field(default_factory=InvoiceParty)

    line_items: list[LineItem] = Field(default_factory=list)

    subtotal: Amount = None

    tax: Amount = None

    discount: Amount = None

    total: Amount = None

    payment_terms: str | None = None

    summary: str = ""

    # Filled in by validate_invoice, never by the model.
    issues: list[str] = Field(default_factory=list)
