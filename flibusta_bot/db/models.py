from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class DownloadedBook(Base):
    __tablename__ = "downloaded_books"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    created_at: Mapped[sa.DateTime] = mapped_column(
        sa.DateTime, nullable=False, server_default=sa.func.now()
    )
    title: Mapped[str] = mapped_column(sa.String, nullable=True)
    url: Mapped[str] = mapped_column(sa.String, nullable=True)
