import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from ...flibusta_parser.schemas import BookDownloadLinks, BookInfoData
from .. import models, schemas


async def get_book_by_id(session: AsyncSession, book_id: int) -> schemas.Book | None:
    book_stmt = sa.select(models.Book).where(models.Book.id == book_id)
    book_res = await session.execute(book_stmt)
    book_record = book_res.scalars().first()
    return schemas.Book.model_validate(book_record) if book_record else None


async def create_book(session: AsyncSession, book: schemas.Book) -> schemas.Book:
    existing = await get_book_by_id(session, book.id)
    if existing:
        return existing
    new_book = models.Book(**book.model_dump(exclude_unset=True))
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return schemas.Book.model_validate(new_book)


async def get_book_info(session: AsyncSession, book_id: int) -> BookInfoData | None:
    book_stmt = sa.select(models.Book).where(models.Book.id == book_id)
    book_res = await session.execute(book_stmt)
    book_record = book_res.scalars().first()

    if not book_record:
        return None

    if not book_record.book_url:
        return None

    # Convert downlad_urls (typo in model) to download_urls with BookDownloadLinks objects
    download_links = [
        BookDownloadLinks(url=f"{book_record.book_url.rstrip('/')}/{i}", format=i)
        for i in ["epub", "fb2", "mobi"]
    ]

    # Create and return BookInfoData
    return BookInfoData(
        id=book_record.id,
        title=book_record.title or "",
        description=book_record.description or "",
        author=book_record.author or "",
        author_url=book_record.author_url or "",
        book_url=book_record.book_url or "",
        download_urls=download_links,
        hashtags=book_record.hashtags,
    )


async def register_downloaded_book(
    session: AsyncSession, book_id: int, format: str | None = None
) -> None:
    downloaded_book = models.DownloadedBook(
        book_id=book_id, format=format
    )
    session.add(downloaded_book)
    await session.commit()
    await session.refresh(downloaded_book)
