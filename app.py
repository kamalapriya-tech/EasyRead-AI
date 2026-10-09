
from flask import Flask, render_template, request
import pymupdf

from nlp.document_reader import extract_document_text
from nlp.keywords import extract_keywords
from nlp.summarizer import summarize_text


app = Flask(__name__)

# Limit uploaded files to 10 MB.
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        uploaded_file = request.files.get("document")

        if not uploaded_file or not uploaded_file.filename:
            error = "Please choose a PDF or Word (.docx) file."

        elif not uploaded_file.filename.lower().endswith((".pdf", ".docx")):
            error = "Only PDF and Word (.docx) files are supported."

        else:
            try:
                document_bytes = uploaded_file.read()

                if not document_bytes:
                    raise ValueError("The uploaded file is empty.")

                text = extract_document_text(
                    uploaded_file.filename,
                    document_bytes
                )

                # Run our NLP components.
                keywords = extract_keywords(text, top_n=10)
                summary = summarize_text(
                    text,
                    sentence_count=5
                )

                result = {
                    "filename": uploaded_file.filename,
                    "page_count": (
                        count_pages(document_bytes)
                        if uploaded_file.filename.lower().endswith(".pdf")
                        else None
                    ),
                    "word_count": len(text.split()),
                    "summary": summary,
                    "keywords": keywords,
                    "text_preview": format_extracted_preview(text[:5000])
                }

            except ValueError as exc:
                error = str(exc)

            except Exception:
                error = (
                    "Could not process this document. "
                    "Please try another valid PDF or Word file."
                )

    return render_template(
        "index.html",
        result=result,
        error=error
    )


def format_extracted_preview(text):
    """Keep standalone bullet markers with their corresponding text."""

    lines = text.splitlines()
    formatted_lines = []
    index = 0

    while index < len(lines):
        if lines[index].strip() == "•":
            next_line = index + 1
            while next_line < len(lines) and not lines[next_line].strip():
                next_line += 1

            if next_line < len(lines):
                formatted_lines.append(
                    f"• {lines[next_line].strip()}"
                )
                index = next_line + 1
                continue

        formatted_lines.append(lines[index])
        index += 1

    return "\n".join(formatted_lines)


def count_pages(pdf_bytes):
    """Return the number of pages in a PDF."""

    with pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:
        return len(document)


@app.errorhandler(413)
def file_too_large(error):
    return (
        "File too large. Please upload a document smaller than 10 MB.",
        413
    )


if __name__ == "__main__":
    app.run(debug=True)