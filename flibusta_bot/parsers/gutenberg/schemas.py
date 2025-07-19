from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from ..schemas import Serializable

@dataclass
class BookListingData(Serializable):
    title: str
    author: str
    url: str


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