from typing import Literal

from pydantic import BaseModel, Field


class RouterResponse(BaseModel):
    """
    Response returned by the Router Agent.
    """

    document_type: Literal[
        "contract",
        "invoice",
        "resume",
        "report",
        "policy",
        "unsupported",
    ]

    workflow: str | None

    supported: bool

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )