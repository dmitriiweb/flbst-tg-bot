from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from loguru import logger

from flibusta_bot.tg_bot import states as bot_states
from flibusta_bot.tg_bot.keyboards import cancels as cancels_keyboard
from flibusta_bot.tg_bot.keyboards import start as start_keyboard

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)


def get_test_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = []
    for i in range(500):
        inline_keyboard.append(
            [
                InlineKeyboardButton(text=str(i), callback_data=f"kb__{i}"),
                InlineKeyboardButton(text=str(i + 1), callback_data=f"kb__{i + 1}"),
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    try:
        await message.answer(
            ("Привет! Я бот для поиска книг в библиотеке. Выберите действие"),
            reply_markup=start_keyboard.get_start_keyboard(),
            # reply_markup=kb_with_pagination(),
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
    await message.answer(
        "Введите название книги",
        reply_markup=cancels_keyboard.single_cansel_kb(),
    )


@router.message(F.text == start_keyboard.SEARCH_BY_AUTHOR_BUTTON)
async def search_by_author(message: Message, state: FSMContext):
    await state.set_state(bot_states.SearchByAuthorStates.search_by_author)
    await message.answer(
        "Введите автора книги",
        reply_markup=cancels_keyboard.single_cansel_kb(),
    )


@router.message(F.text == cancels_keyboard.CANCEL_BUTTON)
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Выберите действие",
        reply_markup=start_keyboard.get_start_keyboard(),
    )


@router.callback_query(F.data == "back")
async def cancel_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if callback.message is None:
        return
    await callback.message.answer(
        "Выберите действие",
        reply_markup=start_keyboard.get_start_keyboard(),
    )


@router.message(StateFilter(None), F.text)
async def default_message(message: Message):
    await message.answer(
        "Выберите действие",
        reply_markup=start_keyboard.get_start_keyboard(),
    )
