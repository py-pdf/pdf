from pathlib import Path

import pytest

import pdf


@pytest.mark.parametrize(
    "pdf_path, password, pages",
    [
        (Path(__file__).parent / "pdflatex-4-pages.pdf", None, 4),
        (
            Path(__file__).parent / "libreoffice-writer-password.pdf",
            "openpassword",
            1,
        ),
    ],
)
def test_document_length(pdf_path, password, pages):
    doc = pdf.PdfFile(pdf_path, password=password)
    assert len(doc) == pages


@pytest.mark.parametrize(
    "pdf_path, password",
    [
        (Path(__file__).parent / "pdflatex-4-pages.pdf", None),
        (
            Path(__file__).parent / "libreoffice-writer-password.pdf",
            "openpassword",
        ),
    ],
)
def test_document_text(pdf_path, password):
    doc = pdf.PdfFile(pdf_path, password=password)
    assert doc.text


@pytest.mark.parametrize(
    "pdf_path, password",
    [
        (Path(__file__).parent / "pdflatex-4-pages.pdf", None),
        (
            Path(__file__).parent / "libreoffice-writer-password.pdf",
            "openpassword",
        ),
    ],
)
def test_document_metadata(pdf_path, password):
    doc = pdf.PdfFile(pdf_path, password=password)
    assert doc.metadata


@pytest.mark.parametrize(
    "pdf_path, password, pages",
    [
        (Path(__file__).parent / "pdflatex-4-pages.pdf", None, 4),
        (
            Path(__file__).parent / "libreoffice-writer-password.pdf",
            "openpassword",
            1,
        ),
    ],
)
def test_iteration(pdf_path, password, pages):
    pages = 0
    doc = pdf.PdfFile(pdf_path, password=password)
    for _page in doc:
        pages += 1
    assert pages == len(doc)


@pytest.mark.parametrize(
    "pdf_path, password, pages",
    [
        (Path(__file__).parent / "pdflatex-4-pages.pdf", None, 4),
        (
            Path(__file__).parent / "libreoffice-writer-password.pdf",
            "openpassword",
            1,
        ),
    ],
)
def test_context_manager(pdf_path, password, pages):
    with pdf.PdfFile(pdf_path, password=password) as doc:
        assert len(doc) == len(doc)
