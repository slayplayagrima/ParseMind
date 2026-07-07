import services
from services.pdf_service import extract_text_from_pdf
from services.pdf_service import extract_text_from_pdf

with open("sample.pdf", "rb") as file:
    pdf_bytes = file.read()

text = extract_text_from_pdf(pdf_bytes)

print("=" * 80)
print(text[:1000])
print("=" * 80)
print(f"\nCharacters extracted: {len(text)}")