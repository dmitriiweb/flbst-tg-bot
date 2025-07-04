from __future__ import annotations

import io
from dataclasses import asdict, dataclass

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
    content: io.BytesIO
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
            f"{self.title} — {self.author}\n "
            f"Скачать книгу: /b{self.book_id}@{config.TG_BOT_NAME}"
        )


@dataclass
class BookDownloadLinks(Serializable):
    url: str
    format: str


@dataclass
class BookInfoData(Serializable):
    id: int
    title: str
    description: str
    author: str
    author_url: str
    book_url: str
    download_urls: list[BookDownloadLinks]
    hashtags: list[str] | None

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["download_urls"] = [link.to_dict() for link in self.download_urls]
        return data

    def to_telegram_message(self) -> str:
        hashtags = (
            " ".join(f"#{tag.title().replace(' ', '')}" for tag in self.hashtags)
            if self.hashtags
            else ""
        )
        return (
            f"<b>{self.title}</b>\n\n"
            f"<i>Автор:</i> {self.author}\n\n"
            f"{hashtags}\n\n"
            f"{self.description}"
        )[:4096]
