from pathlib import Path

from services.document_processor import process_document

pdf_path = Path(__file__).parent.parent / "sample_contract.pdf"

with pdf_path.open("rb") as file:
    pdf_bytes = file.read()

result = process_document(pdf_bytes)

print(result)
