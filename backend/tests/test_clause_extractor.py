from pathlib import Path

from services.pdf_service import extract_text_from_pdf
from skills.clause_extractor import extract_clauses

pdf_path = Path(__file__).parent.parent / "sample_contract.pdf"

with pdf_path.open("rb") as file:
    pdf_bytes = file.read()

text = extract_text_from_pdf(pdf_bytes)

result = extract_clauses(text)

print(result)