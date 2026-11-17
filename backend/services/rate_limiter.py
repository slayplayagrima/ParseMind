import logging
import time

import httpx
from fastapi import HTTPException, Request

from config.settings import settings

logger = logging.getLogger(__name__)

_warned_missing_config = False


def _client_ip(request: Request) -> str:
    """
    Return the caller's IP address.

    Behind Vercel or another proxy, the real client IP is the
    first entry of the X-Forwarded-For header.
    """

    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    if request.client:
        return request.client.host

    return "unknown"


async def _increment(key: str, window_seconds: int) -> int:
    """
    Increment the request counter for a key in Upstash Redis
    and return the new count. The key expires with its window.
    """

    async with httpx.AsyncClient(timeout=3.0) as client:
        response = await client.post(
            f"{settings.UPSTASH_REDIS_REST_URL}/pipeline",
            headers={
                "Authorization": f"Bearer {settings.UPSTASH_REDIS_REST_TOKEN}",
            },
            json=[
                ["INCR", key],
                ["EXPIRE", key, str(window_seconds), "NX"],
            ],
        )

    response.raise_for_status()

    return int(response.json()[0]["result"])


async def enforce_rate_limit(request: Request) -> None:
    """
    FastAPI dependency that limits how many analyses one IP
    can run per window.

    Fails open: if Upstash isn't configured or can't be reached,
    the request is allowed and a warning is logged.
    """

    global _warned_missing_config

    if not settings.UPSTASH_REDIS_REST_URL or not settings.UPSTASH_REDIS_REST_TOKEN:
        if not _warned_missing_config:
            logger.warning("Upstash is not configured. Rate limiting is disabled.")
            _warned_missing_config = True
        return

    window = settings.RATE_LIMIT_WINDOW_SECONDS
    window_id = int(time.time() // window)
    key = f"ratelimit:analyze:{_client_ip(request)}:{window_id}"

    try:
        count = await _increment(key, window)

    except (httpx.HTTPError, KeyError, ValueError, IndexError):
        logger.exception("Rate limiter unavailable. Allowing request.")
        return

    if count > settings.RATE_LIMIT_REQUESTS:
        retry_after = window - int(time.time() % window)

        raise HTTPException(
            status_code=429,
            detail=(
                f"You've reached the limit of {settings.RATE_LIMIT_REQUESTS} "
                "analyses. Please try again later."
            ),
            headers={"Retry-After": str(retry_after)},
        )
