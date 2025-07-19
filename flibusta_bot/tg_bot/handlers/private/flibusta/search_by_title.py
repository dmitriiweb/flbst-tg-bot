from __future__ import annotations

import re
from dataclasses import dataclass

from aiogram import F, Router
from aiogram.enums import ChatAction, ChatType, ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    URLInputFile,
)
from fluentogram import TranslatorRunner  # type: ignore
from loguru import logger

from flibusta_bot import config
from flibusta_bot.parsers.flibusta import schemas
from flibusta_bot.parsers.flibusta.app import App as FlibustaParser
from flibusta_bot.tg_bot import states as bot_states
from flibusta_bot.tg_bot.keyboards.flibusta import (
    choose_download_format_keyboard,
    item_listing_kb,
    one_column_listing,
)
from flibusta_bot.tg_bot.middlewares.i118n import TranslatorRunnerMiddleware

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.message.middleware(TranslatorRunnerMiddleware())
router.callback_query.middleware(TranslatorRunnerMiddleware())

book_id_pattern = re.compile(r"/b/(\d+)")


@dataclass
class FileUrl:
    download_url: str
    filename: str
    format: str
    callback_data: str


@router.message(
    StateFilter(bot_states.FlibustaSearchByTitleStates.search_by_title), F.text
)
async def search_books(
    message: Message, state: FSMContext, i18n: TranslatorRunner, **data
):
    try:
        if message.bot is not None:
            await message.bot.send_chat_action(
                chat_id=message.chat.id, action=ChatAction.TYPING
            )
        if not message.text:
            await message.answer(i18n.search.by.title.empty.query())
            return
        async with FlibustaParser() as parser:
            poges, books = await parser.search_book(message.text)

        if not books:
            await message.answer(i18n.search.by.title.not_.found.title())
            return

        total_books = len(books)
        paginator = item_listing_kb(books, callback_prefix="book")
        kb = await paginator.render_kb()
        await message.answer(
            i18n.search.by.title.found.books(total_books=total_books),
            reply_markup=kb,
        )
        await state.set_state(bot_states.FlibustaSearchByTitleStates.book_selected)
    except Exception as e:
        logger.error(f"search_books error: {e}")
        try:
            await message.answer(i18n.search.by.title.error.generic())
        except Exception:
            pass


@router.callback_query(
    StateFilter(bot_states.FlibustaSearchByTitleStates.book_selected),
    F.data.startswith("book|"),
)
async def get_book_info_handler(callback: CallbackQuery, state: FSMContext, **data):
    i18n = data["i18n"]
    callback_message = callback.message
    callback_data = callback.data
    try:
        if callback_message is None:
            return None
        if callback_data is None:
            return None
        if callback_message.bot is not None:
            await callback_message.bot.send_chat_action(
                chat_id=callback_message.chat.id, action=ChatAction.TYPING
            )
        book_id: str = callback_data.split("|", 1)[-1].split("@")[0]  # type: ignore
        book_info = await _get_book_info(int(book_id), i18n)
        if book_info is None:
            await callback_message.answer(i18n.search.by.title.not_.found.book.info())
            return

        logger.info(
            f"{book_info.id=} {book_info.title=} {book_info.author=} {book_info.book_url=}"
        )
        download_urls = [i.url for i in book_info.download_urls]
        reply_markup = choose_download_format_keyboard(
            download_urls=download_urls,
            download_button_text=i18n.search.by.title.download.button(),
        )
        await callback_message.answer(
            book_info.to_telegram_message(),
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
        )
        await state.set_state(
            bot_states.FlibustaSearchByTitleStates.choose_download_format
        )
    except Exception as e:
        logger.error(f"book_info error: {e}")
        message = callback.message
        if message is None:
            return None
        try:
            await message.answer(i18n.search.by.title.error.generic())
        except Exception:
            pass


@router.callback_query(
    StateFilter(bot_states.FlibustaSearchByTitleStates.choose_download_format),
    F.data.startswith("downloadurl|"),
    F.data.endswith("download"),
)
async def download_book_format(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner, **data
):
    try:
        if callback.data is None:
            return None
        file_url = await _get_file_url(callback.data, callback, i18n)
        if callback.message is None:
            return None

        if callback.message and callback.bot is not None:
            await callback.bot.send_chat_action(
                chat_id=callback.message.chat.id, action=ChatAction.TYPING
            )
        if file_url is None:
            await callback.message.answer(
                i18n.search.by.title.not_.found.download.link()
            )
            return
        answer = i18n.search.by.title.only.one.format(format=file_url.format)
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=i18n.search.by.title.download.button.with_.format(
                            format=file_url.format.lower()
                        ),
                        callback_data=file_url.callback_data,
                    )
                ]
            ]
        )
        await callback.message.answer(answer, reply_markup=kb)
    except Exception as e:
        logger.error(f"download_book_format error: {e}")
        if callback.message is not None:
            try:
                await callback.message.answer(i18n.search.by.title.error.generic())
            except Exception:
                pass


@router.callback_query(
    StateFilter(bot_states.FlibustaSearchByTitleStates.choose_download_format),
    F.data.startswith("downloadurl|"),
)
async def download_book(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner, **data
):
    try:
        callback_data = callback.data
        if callback_data is None:
            return
        if callback.message is None:
            return
        if callback.message and callback.message.bot is not None:
            await callback.message.bot.send_chat_action(
                chat_id=callback.message.chat.id, action=ChatAction.TYPING
            )
        if "downloads" in callback_data:
            callback_data = callback_data.replace("downloads", "download")
        file_url = await _get_file_url(callback_data, callback, i18n)
        if file_url is None:
            await callback.message.answer(
                i18n.search.by.title.not_.found.download.link()
            )
            return
        logger.info(f"{file_url.filename=} {file_url.download_url=}")
        await callback.answer(i18n.search.by.title.download.started())
        doc = URLInputFile(url=file_url.download_url, filename=file_url.filename)
        kb = one_column_listing(
            i18n.start.search.by.title.button(),
            i18n.start.search.by.author.button(),
        )
        if callback.message is not None:
            await callback.message.answer_document(document=doc, reply_markup=kb)
        await state.clear()
    except Exception as e:
        logger.error(f"download_book error: {e}")
        if callback.message is not None:
            try:
                await callback.message.answer(i18n.search.by.title.error.generic())
            except Exception:
                pass


async def _get_file_url(
    callback_data: str, callback: CallbackQuery, i18n: TranslatorRunner
) -> FileUrl | None:
    doc_url = callback_data.split("downloadurl|")[-1]  # type: ignore
    doc_url = f"{config.LIBRARY_BASE_URL}{doc_url}"
    async with FlibustaParser() as parser:
        download_url = await parser.get_download_url(doc_url)
        if download_url is None:
            if callback.message is not None:
                await callback.message.answer(
                    i18n.search.by.title.not_.found.download.link()
                )
            return None
        filename = await parser.get_filename_from_metadata(download_url)
        if filename is None:
            return None
        format_index = -1 if "zip" not in filename else -2
        format = filename.split(".")[format_index]
        # Do not toch, need to correct selecting download book router
        if "download" in callback_data:
            callback_data += "s"
        return FileUrl(
            download_url=download_url,
            filename=filename,
            format=format,
            callback_data=callback_data,
        )


async def _get_book_info(
    book_id: int, i18n: TranslatorRunner, previous_url: str | None = None
) -> schemas.BookInfoData | None:
    try:
        async with FlibustaParser() as parser:
            book_info = await parser.get_book_info(book_id, previous_url)
        return book_info
    except Exception as e:
        logger.error(f"_get_book_info error: {e}")
        return None
