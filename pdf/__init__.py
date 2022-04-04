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

    @property
    def metadata(self) -> Dict[str, Any]:
        # TODO: Can this be made more consistent / nicer?
        # Currently it looks like this:
        # {'/Producer': 'pdfTeX-1.40.23',
        # '/Creator': 'TeX', '/CreationDate': "D:20220403180542+02'00'",
        # '/ModDate': "D:20220403180542+02'00'", '/Trapped': '/False',
        # '/PTEX.Fullbanner': 'This is pdfTeX, Ver...3'}
        return self.reader.getDocumentInfo()  # type: ignore

    def __enter__(self) -> "PdfFile":
        return self

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        self.close()

    def close(self) -> None:
        if self.fp is not None:
            self.fp.close()

    def open(self, name: Any, mode: str = "rb") -> PyPDF2.PdfFileReader:
        return self.reader

    def __getitem__(self, key: int) -> PdfPage:
        return PdfPage(self.reader.getPage(key))

    def __len__(self) -> int:
        return self.reader.getNumPages()  # type: ignore


class PdfFileReader:
    def __init__(self, reader: PyPDF2.PdfFileReader) -> None:
        self.reader = reader
        self.metadata = self.reader.getDocumentInfo()
