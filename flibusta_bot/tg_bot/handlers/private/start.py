from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from loguru import logger

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)


@router.message(Command("start"))
async def cmd_start(message):
    try:
        await message.answer(
            "Привет! Я бот для поиска книг в библиотеке. "
            "Отправь мне название книги и я помогу тебе найти её"
        )
    except Exception as e:
        logger.error(f"cmd_start error: {e}")
        try:
            await message.answer("Извините, произошла ошибка. Попробуйте позже.")
        except Exception:
            pass
