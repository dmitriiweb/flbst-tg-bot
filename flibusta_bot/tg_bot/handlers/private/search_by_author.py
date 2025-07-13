from aiogram import F, Router
from aiogram.enums import ChatAction, ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)
from fluentogram import TranslatorRunner
from loguru import logger

from flibusta_bot import config
from flibusta_bot.flibusta_parser import App as FlibustaParser
from flibusta_bot.tg_bot import states as bot_states
from flibusta_bot.tg_bot.keyboards import item_listing_kb
from flibusta_bot.tg_bot.middlewares.i118n import TranslatorRunnerMiddleware

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.message.middleware(TranslatorRunnerMiddleware())
router.callback_query.middleware(TranslatorRunnerMiddleware())


@router.message(StateFilter(bot_states.SearchByAuthorStates.search_by_author), F.text)
async def search_author(
    message: Message, state: FSMContext, i18n: TranslatorRunner, **data
):
    try:
        if message.bot is not None:
            await message.bot.send_chat_action(
                chat_id=message.chat.id, action=ChatAction.TYPING
            )
        if not message.text:
            await message.answer(i18n.search.by.author.empty.query())
            return
        async with FlibustaParser() as parser:
            authors = await parser.search_authors(message.text)

        if not authors:
            await message.answer(i18n.search.by.author.not_.found.author())
            return

        paginator = item_listing_kb(authors, callback_prefix="author")
        kb = await paginator.render_kb()
        await message.answer(
            i18n.search.by.author.found.authors(total_authors=len(authors)),
            reply_markup=kb,
        )
        await state.set_state(bot_states.SearchByAuthorStates.choose_book)

    except Exception as e:
        logger.error(f"search_author error: {e}")
        try:
            await message.answer(i18n.search.by.author.error.generic())
        except Exception:
            pass


@router.callback_query(
    StateFilter(bot_states.SearchByAuthorStates.choose_book),
    F.data.startswith("author|"),
)
async def choose_book(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner, **data
):
    base_url = config.LIBRARY_BASE_URL.rstrip("/")
    try:
        message = callback.message
        if message is None or not hasattr(message, "text"):
            return
        if message.bot is not None:
            await message.bot.send_chat_action(
                chat_id=message.chat.id, action=ChatAction.TYPING
            )
        if not getattr(message, "text", None):
            await message.answer(i18n.search.by.author.empty.query())  # type: ignore
            return
        author_id = callback.data.split("|")[1] if callback.data else ""  # type: ignore
        author_url = f"{base_url}/a/{author_id}"
        logger.info(f"{author_url=}")
        async with FlibustaParser() as parser:
            _, books = await parser.search_books_by_author(author_url)

        if not books:
            await message.answer(i18n.search.by.author.not_.found.books())  # type: ignore
            return

        total_books = len(books)
        paginator = item_listing_kb(books, callback_prefix="book")
        kb = await paginator.render_kb()
        await state.set_state(bot_states.SearchByTitleStates.book_selected)
        await message.edit_text(
            i18n.search.by.author.found.books(total_books=total_books),
            reply_markup=kb,
        )  # type: ignore
    except Exception as e:
        logger.error(f"search_books error: {e}")
        try:
            if callback.message:
                await callback.message.answer(i18n.search.by.author.error.generic())  # type: ignore
        except Exception:
            pass
