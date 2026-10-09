from pathlib import Path

from nlp.docx_reader import extract_text as extract_docx_text
from nlp.pdf_reader import extract_text as extract_pdf_text


def extract_document_text(filename, document_bytes):
    """Extract readable text from a supported document."""

    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(document_bytes)

    if extension == ".docx":
        return extract_docx_text(document_bytes)

    raise ValueError("Only PDF and Word (.docx) files are supported.")
