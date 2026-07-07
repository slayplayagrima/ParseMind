from pathlib import Path

from services.pdf_service import extract_text_from_pdf
from skills.summarize import summarize

pdf_path = Path(__file__).parent.parent / "sample.pdf"

with pdf_path.open("rb") as file:
    pdf_bytes = file.read()

text = extract_text_from_pdf(pdf_bytes)

summary = summarize(text)

print(summary)