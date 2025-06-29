from sqlalchemy.ext.asyncio import AsyncSession

from .. import models


async def register_downloaded_book(session: AsyncSession, title: str, url: str) -> None:
    downloaded_book = models.DownloadedBook(title=title, url=url)
    session.add(downloaded_book)
    await session.commit()
    await session.refresh(downloaded_book)
