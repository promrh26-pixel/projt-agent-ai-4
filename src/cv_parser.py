"""CV parsing utilities."""
from pathlib import Path
from typing import List

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None


def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF file using PyPDF2."""
    if PdfReader is None:
        raise ImportError("PyPDF2 is required for PDF parsing. Install with pip install PyPDF2")

    text_chunks: List[str] = []
    reader = PdfReader(file_path)
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_chunks.append(page_text)
    return "\n".join(text_chunks)


def extract_texts_from_pdfs(file_paths: List[str]) -> List[str]:
    """Extracts texts from multiple PDF files."""
    return [extract_text_from_pdf(path) for path in file_paths]
