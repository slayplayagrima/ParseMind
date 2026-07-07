from typing import Literal

from pydantic import BaseModel


class Party(BaseModel):
    name: str
    role: str


class PaymentTerms(BaseModel):
    amount: str | None
    currency: str | None
    due_date: str | None
    frequency: str | None


class Clause(BaseModel):
    title: str
    description: str


class Risk(BaseModel):
    title: str
    severity: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ]
    explanation: str
    recommendation: str


class ContractResponse(BaseModel):
    contract_type: str

    title: str

    summary: str

    parties: list[Party]

    effective_date: str | None

    termination_date: str | None

    duration: str | None

    governing_law: str | None

    jurisdiction: str | None

    payment_terms: PaymentTerms | None

    obligations: list[str]

    important_clauses: list[Clause]

    risks: list[Risk]

    recommendations: list[str]