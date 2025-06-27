from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    book_url: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    author: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    author_url: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    description: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    downlad_urls: Mapped[list[dict[str, str]] | None] = mapped_column(
        JSONB, nullable=True
    )
    hashtags: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)

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
    book_id: Mapped[int] = mapped_column(sa.ForeignKey("books.id"))
    format: Mapped[str | None] = mapped_column(sa.String, nullable=True)

    book: Mapped[Book] = relationship("Book", back_populates="downloaded_books")

    def __repr__(self):
        return f"<DownloadedBook(id={self.id}, book_id={self.book_id}, format={self.format})>"
