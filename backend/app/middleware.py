import logging
import time
import uuid

from fastapi import FastAPI, Request

logger = logging.getLogger(__name__)


def register_middlewares(app: FastAPI) -> None:
    """
    Register application middlewares.
    """

    @app.middleware("http")
    async def request_logging_middleware(
        request: Request,
        call_next,
    ):
        request_id = str(uuid.uuid4())[:8]

        start = time.perf_counter()

        logger.info(
            "[%s] %s %s started.",
            request_id,
            request.method,
            request.url.path,
        )

        response = await call_next(request)

        elapsed = time.perf_counter() - start

        logger.info(
            "[%s] %s %s completed in %.2f seconds (%d).",
            request_id,
            request.method,
            request.url.path,
            elapsed,
            response.status_code,
        )

        response.headers["X-Request-ID"] = request_id

        return response