from pathlib import Path

from services.pdf_service import extract_text_from_pdf
from skills.parse_contract import parse_contract

pdf_path = Path(__file__).parent.parent / "sample_contract.pdf"

with pdf_path.open("rb") as file:
    pdf_bytes = file.read()

text = extract_text_from_pdf(pdf_bytes)

result = parse_contract(text)

print(result)