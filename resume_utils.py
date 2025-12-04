from pypdf import PdfReader
from io import BytesIO

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))   # <-- FIXED
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()
