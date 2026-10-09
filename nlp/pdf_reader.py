import pymupdf


def extract_text(pdf_bytes):
    """Extract selectable text from PDF bytes."""

    with pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:

        if document.is_encrypted:
            raise ValueError(
                "Password-protected PDFs are not supported."
            )

        pages = [
            page.get_text("text")
            for page in document
        ]

    text = "\n".join(pages).strip()

    if not text:
        raise ValueError(
            "No readable text found. "
            "This PDF may be scanned and require OCR."
        )

    return text