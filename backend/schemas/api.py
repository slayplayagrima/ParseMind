from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """
    Standard API response returned by every endpoint.
    """

    success: bool

    data: T | None = None

    error: str | None = None