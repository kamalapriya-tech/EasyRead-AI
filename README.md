# EasyRead AI

EasyRead AI is a small Flask web app that extracts text from PDF and Word
documents, then displays a sentence-based summary, keywords, document
statistics, and a preview of the extracted text.

## Features

- Upload PDF (`.pdf`) and Word Open XML (`.docx`) documents.
- Extract selectable text from PDFs with PyMuPDF.
- Extract paragraphs and table rows from Word documents with `python-docx`.
- Generate a five-sentence extractive summary using TF-IDF sentence scores.
  Selected sentences are shown in their original document order.
- Rank up to ten keywords with a pure-Python TF-IDF calculation.
- Show the PDF page count, extracted word count, keywords, and the first
  5,000 characters of extracted text.
- Reformat standalone bullet markers in the extracted-text preview so a bullet
  appears beside its corresponding text.
- Limit uploads to 10 MB.

## Requirements

- Python 3.10 or later
- pip

Python dependencies are listed in [`requirements.txt`](requirements.txt):
Flask, PyMuPDF, `python-docx`, and scikit-learn.

## Setup and run

From the project directory, create and activate a virtual environment in
PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies and start the Flask development server:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser, choose a PDF
or `.docx` file, and select **Analyze document**.

The app also runs directly with the virtual environment's Python executable
without activating it:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

`app.py` starts Flask with debug mode enabled for local development. Do not
expose this development server to the public internet.

## How analysis works

1. The upload form submits the document to the Flask `/` route.
2. The filename extension selects the reader:
   - PDFs are opened with PyMuPDF. Selectable text is collected page by page.
   - Word documents are opened with `python-docx`. Paragraphs and table rows
     are collected in document order.
3. The extracted text is passed to the keyword extractor and summarizer.
4. The results page displays the analysis and a preview of the extracted text.

The summary is **extractive**: it chooses sentences from the source rather
than generating or rewriting new sentences. It splits text at `.`, `!`, and
`?`, scores sentences with scikit-learn's TF-IDF vectorizer, selects up to
five higher-scoring sentences, and returns those selected sentences in source
order. If there are five or fewer sentences, all are returned.

Keywords are ranked using a separate TF-IDF calculation over sentences, with
a built-in stop-word list.

## Supported files and limitations

- Supported: selectable-text PDFs and `.docx` files.
- Not supported: legacy Word `.doc` files, scanned/image-only PDFs, and OCR.
- Password-protected PDFs are not supported.
- PDF page counts are shown; Word documents do not currently report page
  counts.
- Only the first 5,000 characters are shown in the extracted-text preview.
- The upload limit is 10 MB.

The application does not call an external AI service. Document extraction,
summary generation, and keyword extraction run in the Flask application.

## Run tests

Run the test suite from the project directory:

```powershell
python -m unittest discover -s tests -v
```

The tests cover summary sentence ordering, extracted-preview bullet
formatting, PDF and Word uploads, Word table extraction, PDF page counts, and
unsupported file types.

## Project layout

```text
EasyReadAI/
├── app.py                       # Flask app and upload/results route
├── nlp/
│   ├── document_reader.py       # Selects reader by file extension
│   ├── docx_reader.py           # Word paragraph and table extraction
│   ├── keywords.py              # Keyword ranking
│   ├── pdf_reader.py            # PDF text extraction
│   └── summarizer.py            # Extractive sentence summarization
├── static/
│   └── style.css                # Page styling
├── templates/
│   └── index.html               # Upload form and analysis results
├── tests/
│   └── test_document_analysis.py
└── requirements.txt
```
