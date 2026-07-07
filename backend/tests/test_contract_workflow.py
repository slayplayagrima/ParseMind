from pathlib import Path

from agents.router_agent import classify_document
from services.pdf_service import extract_text_from_pdf
from workflows.dispatcher import dispatch_workflow

pdf_path = Path(__file__).parent.parent / "sample_contract.pdf"

with pdf_path.open("rb") as file:
    pdf_bytes = file.read()

document_text = extract_text_from_pdf(pdf_bytes)

router_response = classify_document(document_text)

result = dispatch_workflow(
    router_response,
    document_text,
)

print(result)