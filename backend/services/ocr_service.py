import base64
import logging
from concurrent.futures import ThreadPoolExecutor

import httpx

from config.settings import settings
from services.errors import DocumentError

logger = logging.getLogger(__name__)

# The OCR.space free tier rejects files over 1 MB.
MAX_IMAGE_BYTES = 1024 * 1024

OCR_FAILED_MESSAGE = (
    "We couldn't read this scanned document. Try a clearer scan or a text-based PDF."
)


def ocr_enabled() -> bool:
    return bool(settings.OCR_SPACE_API_KEY)


def _client() -> httpx.Client:
    return httpx.Client(timeout=settings.OCR_TIMEOUT_SECONDS)


def _ocr_image(client: httpx.Client, image: bytes) -> str:
    """
    Send one JPEG page to OCR.space and return its text.
    """

    encoded = base64.b64encode(image).decode()

    response = client.post(
        settings.OCR_SPACE_URL,
        headers={"apikey": settings.OCR_SPACE_API_KEY},
        data={
            "base64Image": f"data:image/jpeg;base64,{encoded}",
            "language": settings.OCR_LANGUAGE,
            # Engine 2 handles mixed layouts, numbers and tables better.
            "OCREngine": "2",
            "scale": "true",
            "detectOrientation": "true",
            "isTable": "true",
        },
    )
    response.raise_for_status()

    payload = response.json()

    if payload.get("IsErroredOnProcessing"):
        raise RuntimeError(f"OCR.space error: {payload.get('ErrorMessage')}")

    results = payload.get("ParsedResults") or []

    return "\n".join(result.get("ParsedText", "") for result in results)


def ocr_pages(images: list[bytes]) -> str:
    """
    OCR page images in parallel and join their text in page order.

    Raises:
        DocumentError: If OCR is not configured or the service fails.
    """

    if not ocr_enabled():
        raise DocumentError(
            "No readable text found in the PDF. The document may be scanned or image-only."
        )

    logger.info("Running OCR on %d page(s).", len(images))

    try:
        with (
            _client() as client,
            ThreadPoolExecutor(max_workers=min(len(images), 4) or 1) as pool,
        ):
            pages = list(pool.map(lambda image: _ocr_image(client, image), images))

    except (httpx.HTTPError, RuntimeError, ValueError) as e:
        # ValueError covers a response that isn't JSON.
        logger.exception("OCR request failed.")
        raise DocumentError(OCR_FAILED_MESSAGE) from e

    return "\n\n".join(pages)


__all__ = [
    "MAX_IMAGE_BYTES",
    "ocr_enabled",
    "ocr_pages",
]
