import os
from pathlib import Path
from typing import Any, Dict, Union

import PyPDF2.pdf


class PdfPage:
    def __init__(self, page: PyPDF2.pdf.PageObject) -> None:
        self.page = page

    @property
    def text(self) -> str:
        return self.page.extractText()  # type: ignore


class PdfFile:
    """
    I want to do this similar to
    https://github.com/python/cpython/blob/3.10/Lib/zipfile.py#L1190
    """

    fp = None

    def __init__(self, file: Union[str, Path], mode: str = "rb") -> None:
        if isinstance(file, os.PathLike):
            file = os.fspath(file)
        if isinstance(file, str):
            fp = open(file, mode)
        self.fp = fp
        self.reader = PyPDF2.PdfFileReader(self.fp)
        self.current_page = 0

    @property
    def metadata(self) -> Dict[str, Any]:
        # TODO: Can this be made more consistent / nicer?
        # Currently it looks like this:
        # {'/Producer': 'pdfTeX-1.40.23',
        # '/Creator': 'TeX', '/CreationDate': "D:20220403180542+02'00'",
        # '/ModDate': "D:20220403180542+02'00'", '/Trapped': '/False',
        # '/PTEX.Fullbanner': 'This is pdfTeX, Ver...3'}
        return self.reader.getDocumentInfo()  # type: ignore

    # Context manager methods
    def __enter__(self) -> "PdfFile":
        return self

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        self.close()

    def close(self) -> None:
        if self.fp is not None:
            self.fp.close()

    def open(self, name: Any, mode: str = "rb") -> PyPDF2.PdfFileReader:
        return self.reader

    # List interface
    def __getitem__(self, key: int) -> PdfPage:
        return PdfPage(self.reader.getPage(key))

    def __len__(self) -> int:
        return self.reader.getNumPages()  # type: ignore

    # Iterator
    def __iter__(self) -> "PdfFile":
        return self

    def __next__(self) -> PdfPage:
        if self.current_page == len(self):
            raise StopIteration
        print(self.current_page)
        self.current_page += 1
        return self[self.current_page - 1]

    # Custom methods
    def text(self) -> str:
        text = ""
        for page in self:
            text += page.text
        return text


class PdfFileReader:
    def __init__(self, reader: PyPDF2.PdfFileReader) -> None:
        self.reader = reader
        self.metadata = self.reader.getDocumentInfo()
