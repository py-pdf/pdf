import datetime
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Union

import PyPDF2.pdf


@dataclass
class Metadata:
    title: Optional[str] = None
    producer: Optional[str] = None
    creator: Optional[str] = None
    creation_date: Optional[datetime.datetime] = None
    modification_date: Optional[datetime.datetime] = None
    other: Optional[Dict[str, Any]] = None


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

    def __init__(
        self,
        file: Union[str, Path],
        mode: str = "rb",
        password: Optional[str] = None,
    ) -> None:
        if isinstance(file, os.PathLike):
            file = os.fspath(file)
        if isinstance(file, str):
            fp = open(file, mode)
        self.fp = fp
        self.password = password
        self.reader = PyPDF2.PdfFileReader(self.fp)

        if self.reader.isEncrypted and self.password is not None:
            self.reader.decrypt(self.password)
        self.current_page = 0

    @property
    def metadata(self) -> Metadata:
        metadict = self.reader.getDocumentInfo()
        data = dict(metadict)
        meta = Metadata()
        meta.producer = data.get("/Producer")
        meta.creator = data.get("/Creator")
        if "/CreationDate" in data:
            meta.creation_date = datestr_to_datetime(data["/CreationDate"])
        if "/ModDate" in data:
            meta.modification_date = datestr_to_datetime(data["/ModDate"])
        meta.other = {}
        for key in data:
            if key in ["/Producer", "/Creator"]:
                continue
            meta.other[key] = metadict[key]
        return meta

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
    @property
    def text(self) -> str:
        text = ""
        for page in self:
            text += page.text
        return text


def datestr_to_datetime(d: str) -> datetime.datetime:
    if d.startswith("D:"):
        d = d[2:]
    if "'" in d:
        d = d[:-7]  # Strip offset - we lose information here!
    return datetime.datetime.strptime(d, "%Y%m%d%H%M%S")
