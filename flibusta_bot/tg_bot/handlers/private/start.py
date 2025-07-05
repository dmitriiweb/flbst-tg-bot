from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from loguru import logger
from aiogram import F, Router
from aiogram.enums import ChatType, ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from flibusta_bot.tg_bot.keyboards import start as start_keyboard
from flibusta_bot.tg_bot import states as bot_states

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    try:
        await message.answer(
            (
                "Привет! Я бот для поиска книг в библиотеке. "
                "Отправь мне название книги и я помогу тебе найти её"
            ),
            reply_markup=start_keyboard.get_start_keyboard(),
        )
    except Exception as e:
        logger.error(f"cmd_start error: {e}")
        try:
            await message.answer("Извините, произошла ошибка. Попробуйте позже.")
        except Exception:
            pass


@router.message(F.text == start_keyboard.SEARCH_BY_TITLE_BUTTON)
async def search_by_title(message: Message, state: FSMContext):
    await state.set_state(bot_states.SearchByTitleStates.search_by_title)
    await message.answer("Введите название книги")


@router.message(F.text == start_keyboard.SEARCH_BY_AUTHOR_BUTTON)
async def search_by_author(message: Message, state: FSMContext):
    await state.set_state(bot_states.SearchByAuthorStates.search_by_author)
    await message.answer("Введите автора книги")