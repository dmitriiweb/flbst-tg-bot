from __future__ import annotations

from dataclasses import dataclass

from ..schemas import Serializable


@dataclass
class BookListingData(Serializable):
    title: str
    author: str
    url: str

    @property
    def book_id(self) -> str:
        return self.url.split("/")[-1]


@dataclass
class BookInfoData(Serializable):
    title: str
    author: str
    url: str
    description: str
    download_urls: list[DownloadUrlData]


@dataclass
class DownloadUrlData(Serializable):
    title: str
    url: str

    @property
    def file_format(self) -> str:
        """Extract normalized filename from the URL"""
        raw_filename = self.url.split("/")[-1]
        if raw_filename.endswith(".zip"):
            return "zip"
        return raw_filename.split(".")[-2]

    @property
    def download_file_format(self) -> str:
        raw_filename = self.url.split("/")[-1]
        if raw_filename.endswith(".zip"):
            return "zip"
        return ".".join(raw_filename.split(".")[1:-1])
