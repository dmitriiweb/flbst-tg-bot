from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from fluentogram import TranslatorRunner
from loguru import logger

from flibusta_bot.tg_bot import states as bot_states
from flibusta_bot.tg_bot.filters.i18n_filter import I18nFilter
from flibusta_bot.tg_bot.keyboards import cancels as cancels_keyboard
from flibusta_bot.tg_bot.keyboards import start as start_keyboard
from flibusta_bot.tg_bot.middlewares.i118n import TranslatorRunnerMiddleware

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.message.middleware(TranslatorRunnerMiddleware())


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


@router.message(CommandStart())
async def cmd_start(
    message: Message, state: FSMContext, i18n: TranslatorRunner, **data
):
    await state.clear()
    try:
        await message.answer(
            i18n.start.greeting(),
            reply_markup=start_keyboard.get_start_keyboard(
                i18n.start.search.by.title.button(),
                i18n.start.search.by.author.button(),
            ),
        )
    except Exception as e:
        logger.error(f"cmd_start error: {e}")
        try:
            await message.answer(i18n.start.error.generic())
        except Exception:
            pass


@router.message(I18nFilter("start-search-by-title-button"))
async def search_by_title(
    message: Message, state: FSMContext, i18n: TranslatorRunner, **data
):
    await state.set_state(bot_states.SearchByTitleStates.search_by_title)
    await message.answer(
        i18n.start.enter.title(),
        reply_markup=cancels_keyboard.single_cansel_kb(i18n.cancel.button()),
    )


@router.message(I18nFilter("start-search-by-author-button"))
async def search_by_author(
    message: Message, state: FSMContext, i18n: TranslatorRunner, **data
):
    await state.set_state(bot_states.SearchByAuthorStates.search_by_author)
    await message.answer(
        i18n.start.enter.author(),
        reply_markup=cancels_keyboard.single_cansel_kb(i18n.cancel.button()),
    )


@router.message(I18nFilter("cancel-button"))
async def cancel(message: Message, state: FSMContext, i18n: TranslatorRunner, **data):
    await state.clear()
    await message.answer(
        i18n.start.choose.action(),
        reply_markup=start_keyboard.get_start_keyboard(
            i18n.start.search.by.title.button(),
            i18n.start.search.by.author.button(),
        ),
    )


@router.callback_query(F.data == "back")
async def cancel_callback(callback: CallbackQuery, state: FSMContext, **data):
    i18n = data["i18n"]
    await state.clear()
    if callback.message is None:
        return
    await callback.message.answer(
        i18n.start.choose.action(),
        reply_markup=start_keyboard.get_start_keyboard(
            i18n.start.search.by.title.button(),
            i18n.start.search.by.author.button(),
        ),
    )


@router.message(StateFilter(None), F.text)
async def default_message(message: Message, i18n: TranslatorRunner, **data):
    await message.answer(
        i18n.start.choose_action(),
        reply_markup=start_keyboard.get_start_keyboard(
            i18n.start.search.by.title.button(),
            i18n.start.search.by.author.button(),
        ),
    )
