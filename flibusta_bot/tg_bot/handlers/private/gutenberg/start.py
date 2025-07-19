from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner  # type: ignore
from loguru import logger

from flibusta_bot.parsers.gutenberg.app import App as GutenbergParser
from flibusta_bot.tg_bot.filters.i18n_filter import I18nFilter
from flibusta_bot.tg_bot.keyboards import gutenberg as kbs
from flibusta_bot.tg_bot.middlewares.i118n import TranslatorRunnerMiddleware
from flibusta_bot.tg_bot.states import GutenbergStartStates

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.message.middleware(TranslatorRunnerMiddleware())
router.callback_query.middleware(TranslatorRunnerMiddleware())


@router.message(I18nFilter("start-choose-library-gutenberg"))
async def choose_library_gutenberg(
    message: Message, state: FSMContext, i18n: TranslatorRunner, **data
):
    kb = kbs.cancel_button(i18n.cancel.button())
    answer = i18n.gutetenberg.call.to.action()
    await message.answer(answer, reply_markup=kb)
    await state.set_state(GutenbergStartStates.search_query)


@router.message(StateFilter(GutenbergStartStates.search_query), F.text)
async def search_query(
    message: Message, state: FSMContext, i18n: TranslatorRunner, **data
):
    async with GutenbergParser() as parser:
        books, next_index, prev_index = await parser.search_books(message.text)
    kb = kbs.book_listing_kb(books, prev_index, next_index, i18n)
    await message.answer(
        i18n.gutenberg.listing.book.title(query=message.text), reply_markup=kb
    )
    logger.debug(f"{next_index=}, {prev_index=}, {message.text=}")
    await state.update_data(user_query=message.text)


@router.callback_query(
    StateFilter(GutenbergStartStates.search_query), F.data.startswith("nav_button")
)
async def listing_navigation(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner, **data
):
    start_index = callback.data.split("|")[-1]
    state_data = await state.get_data()
    user_query = state_data.get("user_query")
    async with GutenbergParser() as parser:
        books, next_index, prev_index = await parser.search_books(
            user_query, start_index
        )
    logger.debug(f"{next_index=}, {prev_index=}, {user_query=}, {start_index=}")
    kb = kbs.book_listing_kb(books, prev_index, next_index, i18n)
    await callback.message.answer(
        i18n.gutenberg.listing.book.title(query=user_query), reply_markup=kb
    )
