from datetime import datetime

from pydantic import BaseModel


class NewUser(BaseModel):
    user_id: int
    username: str | None

    model_config = {"extra": "ignore"}


class User(NewUser):
    created_at: datetime

    model_config = {"from_attributes": True}


class NewBook(BaseModel):
    library_id: str | None = None
    title: str | None = None
    book_url: str | None = None
    author: str | None = None
    author_url: str | None = None
    description: str | None = None

    model_config = {"extra": "ignore"}


class Book(NewBook):
    id: int

    model_config = {"from_attributes": True}
