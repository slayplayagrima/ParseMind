from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from config.settings import settings
from schemas.api import APIResponse
from services.document_processor import process_document
from services.rate_limiter import enforce_rate_limit

router = APIRouter()


@router.post(
    "/analyze",
    dependencies=[Depends(enforce_rate_limit)],
)
async def analyze_document(
    file: UploadFile = File(...),
):
    """
    Analyze an uploaded PDF document.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024

    pdf_bytes = await file.read(max_bytes + 1)

    if len(pdf_bytes) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File is too large. The limit is {settings.MAX_UPLOAD_MB} MB.",
        )

    if not pdf_bytes.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF.",
        )

    # The pipeline makes blocking Groq and PyMuPDF calls, so run it in a
    # worker thread to keep the event loop free for other requests.
    result = await run_in_threadpool(process_document, pdf_bytes)

    return APIResponse(
        success=True,
        data=result,
    )