from datetime import datetime

from pydantic import BaseModel


class NewUser(BaseModel):
    user_id: int
    username: str | None

    model_config = {"extra": "ignore"}


class User(NewUser):
    created_at: datetime

    model_config = {"from_attributes": True}


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


