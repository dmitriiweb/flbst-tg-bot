from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from flibusta_bot import config


@dataclass
class Serializable:
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Serializable:
        return cls(**data)


@dataclass
class HttpResponse(Serializable):
    status_code: int
    content: str
    headers: dict
    url: str


@dataclass
class BinaryHttpResponse:
    status_code: int
    content: bytes
    headers: dict
    url: str


@dataclass
class BookListingData(Serializable):
    title: str
    book_url: str
    author: str
    author_url: str

    @property
    def book_id(self) -> str:
        return self.book_url.split("/")[-1]

    def __str__(self) -> str:
        return (
            f"{self.title} - {self.author}\n "
            f"Скачать книгу: /b{self.book_id}@{config.TG_BOT_NAME}"
        )


@dataclass
class BookInfoData(BookListingData):
    description: str
    download_urls: list[BookDownloadLinks]

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["download_urls"] = [link.to_dict() for link in self.download_urls]
        return data


BookFormat = Literal["epub", "fb2", "mobi"]


@dataclass
class BookDownloadLinks(Serializable):
    url: str
    format: BookFormat
