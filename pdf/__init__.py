import datetime
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, TypeVar, Union

import PyPDF2.pdf


@dataclass
class Metadata:
    # What is the doucment about?
    title: Optional[str] = None
    subject: Optional[str] = None
    keywords: Optional[str] = None

    # Who created it when?
    author: Optional[str] = None
    creation_date: Optional[datetime.datetime] = None
    modification_date: Optional[datetime.datetime] = None

    # How was the document created?
    producer: Optional[str] = None
    creator: Optional[str] = None

    # More information
    other: Optional[Dict[str, Any]] = None


@dataclass
class Links:
    page: int
    text: Optional[str] = None


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
        meta.title = data.get("/Title")
        meta.subject = data.get("/Subject")
        meta.keywords = data.get("/Keywords")
        meta.author = data.get("/Author")
        if "/CreationDate" in data:
            meta.creation_date = datestr_to_datetime(data["/CreationDate"])
        if "/ModDate" in data:
            meta.modification_date = datestr_to_datetime(data["/ModDate"])
        meta.producer = data.get("/Producer")
        meta.creator = data.get("/Creator")
        meta.other = {}
        for key in data:
            if key in [
                "/Title",
                "/Subject",
                "/Keywords",
                "/Author",
                "/Producer",
                "/Creator",
            ]:
                continue
            meta.other[key] = metadict[key]
        return meta

    @property
    def outline(self) -> List[Links]:
        captured = []
        outlines = self.reader.getOutlines()
        for ol in iter_page(outlines):
            captured.append(
                Links(
                    page=self.reader.getDestinationPageNumber(ol),
                    text=ol.title,
                )
            )
        return captured

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


T = TypeVar("T")


def iter_page(
    iterable_or_page: Union[T, List[T], List[List[T]]]
) -> Iterator[T]:
    if isinstance(iterable_or_page, list):
        for inner in iterable_or_page:
            yield from iter_page(inner)
    else:
        yield iterable_or_page
