from aiogram import Router
from aiogram.filters.command import Command

router = Router()


@router.message(Command("start"))
async def cmd_start(message):
    await message.answer(
        "Привет! Я бот для поиска книг в библиотеке. "
        "Отправь мне название книги или автора, и я помогу тебе найти нужную информацию."
    )
