from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from config.settings import settings
from schemas.api import APIResponse
from services.document_processor import process_document
from services.file_types import detect_file_type
from services.rate_limiter import enforce_rate_limit

router = APIRouter()


@router.post(
    "/analyze",
    dependencies=[Depends(enforce_rate_limit)],
)
async def analyze_document(
    file: Annotated[UploadFile, File()],
):
    """
    Analyze an uploaded PDF, Word (.docx) or text file.
    """

    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024

    data = await file.read(max_bytes + 1)

    if len(data) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File is too large. The limit is {settings.MAX_UPLOAD_MB} MB.",
        )

    file_type = detect_file_type(data, file.filename, file.content_type)

    # The pipeline makes blocking Groq and parsing calls, so run it in a
    # worker thread to keep the event loop free for other requests.
    result = await run_in_threadpool(process_document, data, file_type)

    return APIResponse(
        success=True,
        data=result,
    )
