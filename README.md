[![PyPI version](https://badge.fury.io/py/pdffile.svg)](https://badge.fury.io/py/pdffile)
[![Code](https://img.shields.io/badge/code-GitHub-brightgreen)](https://github.com/py-pdf/pdf)
[![Actions Status](https://github.com/py-pdf/pdf/workflows/Unit%20Tests/badge.svg)](https://github.com/py-pdf/pdf/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# pdf
A modern pure-Python library for reading PDF files.

The goal is to have a modern interface to handle PDF files which is consistent
with itself and typical Python syntax.

The library should be Python-only (hence no C-extensions), but allow to change
the backend. Similar in concept to [matplotlib backends](https://matplotlib.org/2.0.2/faq/usage_faq.html#what-is-a-backend) and [Keras backends](https://faroit.com/keras-docs/1.2.0/backend/).

The default backend could be PyPDF2.

Possible other backends could be [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
(using [MuPDF](https://mupdf.com/))
and [PikePDF](https://github.com/pikepdf/pikepdf) (using [QPDF](https://github.com/qpdf/qpdf)).

> **WARNING**: This library is UNSTABLE at the moment! Expect many changes!

## Installation

```bash
pip install pdffile
```

## Usage


### Retrieve Metadata

```pycon
>>> import pdf

>>> doc = pdf.PdfFile("001-trivial/minimal-document.pdf")
>>> len(doc)
1

>>> doc.metadata
Metadata(
    title=None,
    producer='pdfTeX-1.40.23',
    creator='TeX',
    creation_date=datetime.datetime(2022, 4, 3, 18, 5, 42),
    modification_date=datetime.datetime(2022, 4, 3, 18, 5, 42)
    other={
         '/CreationDate': "D:20220403180542+02'00'",
         '/ModDate': "D:20220403180542+02'00'",
         '/Trapped': '/False',
         '/PTEX.Fullbanner': 'This is pdfTeX, V...'})

```

### Encrypted PDFs

If you have an encrypted PDF, just provide the key:

```python
doc = pdf.PdfFile(pdf_path, password=password)
```

All following operations work just as described.


## Get Outline

```pycon
>>> import pdf
>>> doc = pdf.PdfFile(pdf_path, password=password)
>>> doc.outline
[
    Links(page=5, text='1 Header'),
    Links(page=5, text='1.1 A section'),
    Links(page=9, text='2 Foobar'),
    Links(page=108, text='References')
]
```

### Extract Text

```pycon
>>> import pdf
>>> doc = pdf.PdfFile("001-trivial/minimal-document.pdf")
>>> doc[0]
<pdf.PdfPage object at 0x7f72d2b04100>
>>> doc[0].text
'Loremipsumdolorsitamet,consetetursadipscingelitr,seddiamnonumyeirmod\ntemporinviduntutlaboreetdoloremagnaaliquyamerat,seddiamvoluptua.Atvero\neosetaccusametjustoduodoloresetearebum.Stetclitakasdgubergren,noseataki-\nmatasanctusestLoremipsumdolorsitamet.Loremipsumdolorsitamet,consetetur\nsadipscingelitr,seddiamnonumyeirmodtemporinviduntutlaboreetdoloremagna\naliquyamerat,seddiamvoluptua.Atveroeosetaccusametjustoduodoloresetea\nrebum.Stetclitakasdgubergren,noseatakimatasanctusestLoremipsumdolorsit\namet.\n1\n'
```

Alternatively, you can use `doc.text` to get the text of all pages.
