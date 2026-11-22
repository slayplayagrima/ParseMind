from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, Field

SEVERITIES = ("low", "medium", "high", "critical")


def _normalize_severity(value: object) -> str:
    """
    Models sometimes answer "High" or "moderate". Map those onto our scale.
    """

    text = str(value or "").strip().lower()

    if text in SEVERITIES:
        return text

    return {"moderate": "medium", "severe": "high", "minor": "low"}.get(text, "medium")


Severity = Annotated[
    Literal["low", "medium", "high", "critical"],
    BeforeValidator(_normalize_severity),
]


class PolicyRule(BaseModel):
    title: str
    description: str


class ComplianceGap(BaseModel):
    title: str
    severity: Severity
    explanation: str
    recommendation: str


class PolicyResponse(BaseModel):
    title: str | None = None

    policy_type: str | None = None

    organization: str | None = None

    effective_date: str | None = None

    version: str | None = None

    scope: str | None = None

    applies_to: list[str] = Field(default_factory=list)

    rules: list[PolicyRule] = Field(default_factory=list)

    obligations: list[str] = Field(default_factory=list)

    prohibited: list[str] = Field(default_factory=list)

    penalties: list[str] = Field(default_factory=list)

    compliance_gaps: list[ComplianceGap] = Field(default_factory=list)

    summary: str = ""
