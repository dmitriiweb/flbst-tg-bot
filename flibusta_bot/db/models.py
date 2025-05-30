from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str | None] = mapped_column(sa.String, nullable=True)

    downloaded_books: Mapped[list[DownloadedBook]] = relationship(
        "DownloadedBook", back_populates="user"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    library_id: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    title: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    book_url: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    author: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    author_url: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    description: Mapped[str | None] = mapped_column(sa.Text, nullable=True)

    downloaded_books: Mapped[list[DownloadedBook]] = relationship(
        "DownloadedBook", back_populates="book"
    )

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author})>"


class DownloadedBook(Base):
    __tablename__ = "downloaded_books"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    created_at: Mapped[sa.DateTime] = mapped_column(
        sa.DateTime, nullable=False, server_default=sa.func.now()
    )
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(sa.ForeignKey("books.id"))
    format: Mapped[str | None] = mapped_column(sa.String, nullable=True)

    user: Mapped[User] = relationship("User", back_populates="downloaded_books")
    book: Mapped[Book] = relationship("Book", back_populates="downloaded_books")

    def __repr__(self):
        return f"<DownloadedBook(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, format={self.format})>"
