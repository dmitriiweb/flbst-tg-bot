import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas


async def get_book_by_id(session: AsyncSession, book_id: int) -> schemas.Book | None:
    book_stmt = sa.select(models.Book).where(models.Book.id == book_id)
    book_res = await session.execute(book_stmt)
    book_record = book_res.scalars().first()
    return schemas.Book.model_validate(book_record) if book_record else None


async def create_book(session: AsyncSession, book: schemas.Book) -> schemas.Book:
    new_book = models.Book(**book.model_dump(exclude_unset=True))
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return schemas.Book.model_validate(new_book)


async def register_downloaded_book(
    session: AsyncSession, user_id: int, book_id: int, format: str | None = None
) -> None:
    downloaded_book = models.DownloadedBook(
        user_id=user_id, book_id=book_id, format=format
    )
    session.add(downloaded_book)
    await session.commit()
    await session.refresh(downloaded_book)


async def update_book_description(
    session: AsyncSession, library_id: str, description: str
) -> None:
    stmt = (
        sa.update(models.Book)
        .where(models.Book.id == library_id)
        .values(description=description)
    )
    await session.execute(stmt)
    await session.commit()
