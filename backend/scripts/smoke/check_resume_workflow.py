from pathlib import Path

from agents.router_agent import classify_document
from services.pdf_service import extract_text_from_pdf
from workflows.dispatcher import dispatch_workflow

# Path to the sample PDF
pdf_path = Path(__file__).parent / "sample.pdf"

# Read PDF
with pdf_path.open("rb") as file:
    pdf_bytes = file.read()

# Extract text
document_text = extract_text_from_pdf(pdf_bytes)

# Route the document
router_response = classify_document(document_text)

# Execute the correct workflow
result = dispatch_workflow(router_response, document_text)

# Print the final analysis
print(result)