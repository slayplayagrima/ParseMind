from fastapi import APIRouter, File, HTTPException, UploadFile

from schemas.api import APIResponse
from services.document_processor import process_document

router = APIRouter()


@router.post("/analyze")
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

    pdf_bytes = await file.read()

    result = process_document(pdf_bytes)

    return APIResponse(
        success=True,
        data=result,
    )