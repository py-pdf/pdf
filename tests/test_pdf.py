from pathlib import Path

import pdf

pdf_path = Path(__file__).parent / "pdflatex-4-pages.pdf"


def test_document_length():
    doc = pdf.PdfFile(pdf_path)
    assert len(doc) == 4


def test_iteration():
    pages = 0
    doc = pdf.PdfFile(pdf_path)
    for page in doc:
        pages += 1
    assert pages == len(doc)
