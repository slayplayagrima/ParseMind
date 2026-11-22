from pydantic import BaseModel, Field


class ReportMetric(BaseModel):
    name: str
    value: str
    context: str | None = None


class ReportResponse(BaseModel):
    title: str | None = None

    report_type: str | None = None

    authors: list[str] = Field(default_factory=list)

    organization: str | None = None

    publication_date: str | None = None

    purpose: str | None = None

    key_findings: list[str] = Field(default_factory=list)

    metrics: list[ReportMetric] = Field(default_factory=list)

    conclusions: list[str] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)

    limitations: list[str] = Field(default_factory=list)

    summary: str = ""
