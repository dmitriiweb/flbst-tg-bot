from aiogram import F, Router
from aiogram.enums import ChatAction, ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)
from loguru import logger

from flibusta_bot import config
from flibusta_bot.flibusta_parser import App as FlibustaParser
from flibusta_bot.tg_bot import states as bot_states
from flibusta_bot.tg_bot.keyboards import item_listing_kb

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)


@router.message(StateFilter(bot_states.SearchByAuthorStates.search_by_author), F.text)
async def search_author(message: Message, state: FSMContext):
    try:
        if message.bot is not None:
            await message.bot.send_chat_action(
                chat_id=message.chat.id, action=ChatAction.TYPING
            )
        if not message.text:
            await message.answer("Пустой запрос.")
            return
        async with FlibustaParser() as parser:
            authors = await parser.search_authors(message.text)

        if not authors:
            answer = (
                "К сожалению, не удалось найти ни одного автора.\n\n"
                "Попробуйте найти автора по другому запросу "
                "или нажмите кнопку Отмена"
            )
            await message.answer(answer)
            return

        paginator = item_listing_kb(authors, callback_prefix="author")
        kb = await paginator.render_kb()
        await message.answer(
            f"Найдено {len(authors)} авторов:\n\n",
            reply_markup=kb,
        )
        await state.set_state(bot_states.SearchByAuthorStates.choose_book)

    except Exception as e:
        logger.error(f"search_author error: {e}")
        try:
            await message.answer("Извините, произошла ошибка. Попробуйте позже.")
        except Exception:
            pass


@router.callback_query(
    StateFilter(bot_states.SearchByAuthorStates.choose_book),
    F.data.startswith("author|"),
)
async def choose_book(callback: CallbackQuery, state: FSMContext):
    base_url = config.LIBRARY_BASE_URL.rstrip("/")
    try:
        message = callback.message
        if message is None:
            return
        if message.bot is not None:
            await message.bot.send_chat_action(
                chat_id=message.chat.id, action=ChatAction.TYPING
            )
        if not message.text:
            await message.answer("Пустой запрос.")
            return
        author_id = callback.data.split("|")[1]
        author_url = f"{base_url}/a/{author_id}"
        logger.info(f"{author_url=}")
        async with FlibustaParser() as parser:
            _, books = await parser.search_books_by_author(author_url)

        if not books:
            answer = "К сожалению, не удалось найти ни одной книги."
            await message.answer(answer)
            return

        total_books = len(books)
        paginator = item_listing_kb(books, callback_prefix="book")
        kb = await paginator.render_kb()
        await state.set_state(bot_states.SearchByTitleStates.book_selected)
        await message.edit_text(
            f"Найдено {total_books} книг:\n\n",
            reply_markup=kb,
        )
    except Exception as e:
        logger.error(f"search_books error: {e}")
        try:
            await callback.message.answer(
                "Извините, произошла ошибка. Попробуйте позже."
            )
        except Exception:
            pass
