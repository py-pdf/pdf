from pathlib import Path

import pdf


def test_document_length():
    path = Path(__file__).parent / "pdflatex-4-pages.pdf"
    doc = pdf.PdfFile(path)
    assert len(doc) == 4
