from pathlib import Path

from agents.router_agent import classify_document
from services.pdf_service import extract_text_from_pdf

pdf_path = Path(__file__).parent.parent / "sample.pdf"

with pdf_path.open("rb") as file:
    pdf_bytes = file.read()

text = extract_text_from_pdf(pdf_bytes)

result = classify_document(text)

print(result)