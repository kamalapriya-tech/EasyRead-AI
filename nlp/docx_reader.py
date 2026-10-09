from io import BytesIO

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph


def extract_text(docx_bytes):
    """Extract paragraph and table text from a Word document."""

    document = Document(BytesIO(docx_bytes))
    blocks = []

    for item in document.iter_inner_content():
        if isinstance(item, Paragraph):
            text = item.text.strip()
            if text:
                blocks.append(text)
        elif isinstance(item, Table):
            for row in item.rows:
                cells = [
                    cell.text.strip()
                    for cell in row.cells
                    if cell.text.strip()
                ]
                if cells:
                    blocks.append(" | ".join(cells))

    text = "\n".join(blocks).strip()

    if not text:
        raise ValueError("No readable text found in this Word document.")

    return text
