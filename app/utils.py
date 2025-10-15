import re
from pdfminer.high_level import extract_text

def extract_text_from_pdf(path: str) -> str:
    return extract_text(path)

def clean_text(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        chunk = ' '.join(tokens[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks
