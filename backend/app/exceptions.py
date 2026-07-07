import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from schemas.api import APIResponse

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        response = APIResponse(
            success=False,
            error=str(exc.detail),
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump(),
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
        message = str(exc)

        status = 500
        error = "Internal server error."

        if message == "RATE_LIMIT_EXCEEDED":
            status = 429
            error = (
                "AI service rate limit exceeded. "
                "Please try again later."
            )

        logger.exception("Unhandled exception.", exc_info=exc)

        response = APIResponse(
            success=False,
            error=error,
        )

        return JSONResponse(
            status_code=status,
            content=response.model_dump(),
        )