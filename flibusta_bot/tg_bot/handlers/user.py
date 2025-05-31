from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    Message,
)
from loguru import logger

from flibusta_bot.db import db_session, storage
from flibusta_bot.flibusta_parser import App as FlibustaParser

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)




@router.message(Command("start"))
async def cmd_start(message):
    async with db_session() as session:
        _ = await storage.users.get_or_create_user(
            session, message.from_user.id, message
        )
    await message.answer(
        "Привет! Я бот для поиска книг в библиотеке. "
        "Отправь мне название книги или автора, и я помогу тебе найти нужную информацию."
    )


@router.message(F.text.startswith("/b"))
async def book_info(message: Message):
    book_id: str = message.text.split("/b", 1)[-1].split("@")[0]  # type: ignore
    async with FlibustaParser() as parser:
        book_info = await parser.get_book_info(book_id, message.text)


@router.message(F.text)
async def search_books(message: Message):
    async with FlibustaParser() as parser:
        poges, books = await parser.search_book(message.text)

    if not books:
        answer = "К сожалению, не удалось найти ни одной книги."
        await message.answer(answer)
        return

    books = books[:10]
    total_books = len(books)
    answer = f"Найдено {total_books} книг:\n\n"
    books_list = [str(i) for i in books]
    books_text = "\n\n".join(books_list)
    answer += books_text
    await message.answer(answer)
