from datetime import datetime

from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str | None = None
    book_url: str | None = None
    author: str | None = None
    author_url: str | None = None
    description: str | None = None
    download_urls: list[dict[str, str]] | None = None
    hashtags: list[str] | None = None

    model_config = {"extra": "ignore", "from_attributes": True}
