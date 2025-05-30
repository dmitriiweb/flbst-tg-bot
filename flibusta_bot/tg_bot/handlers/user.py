from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.enums import ChatType

from flibusta_bot.db import db_session, storage

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


@router.message(F.text)
async def search_books(message: Message):
    pass
