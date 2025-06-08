import re

from aiogram import F, Router
from aiogram.enums import ChatAction, ChatType, ParseMode
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    Message,
    URLInputFile,
)
from loguru import logger

from flibusta_bot import config
from flibusta_bot.db import db_session, storage
from flibusta_bot.db.schemas import Book as BookSchema
from flibusta_bot.db.storage.books import create_book
from flibusta_bot.flibusta_parser import App as FlibustaParser
from flibusta_bot.flibusta_parser.schemas import BookInfoData
from flibusta_bot.tg_bot.keyboards import choose_download_format_keyboard

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)

book_id_pattern = re.compile(r"/b/(\d+)")


@router.message(Command("start"))
async def cmd_start(message):
    async with db_session() as session:
        _ = await storage.users.get_or_create_user(
            session, message.from_user.id, message
        )
    await message.answer(
        "Привет! Я бот для поиска книг в библиотеке. "
        "Отправь мне название книги и я помогу тебе найти её"
    )


@router.message(F.text.startswith("/b"), F.text.endswith(config.TG_BOT_NAME))
async def book_info(message: Message):
    if message.bot is not None:
        await message.bot.send_chat_action(
            chat_id=message.chat.id, action=ChatAction.TYPING
        )
    book_id: str = message.text.split("/b", 1)[-1].split("@")[0]  # type: ignore
    book_info = await _get_book_info(int(book_id), message)
    if book_info is None:
        await message.answer(
            "К сожалению, не удалось найти информацию о книге с таким ID."
        )
        return

    download_urls = [i.url for i in book_info.download_urls]
    reply_markup = choose_download_format_keyboard(download_urls=download_urls)
    await message.answer(
        book_info.to_telegram_message(),
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


@router.callback_query(F.data.startswith("downloadurl:"))
async def download_book(callback: CallbackQuery):
    if callback.message and callback.bot is not None:
        await callback.bot.send_chat_action(
            chat_id=callback.message.chat.id, action=ChatAction.TYPING
        )
    doc_url = callback.data.split("downloadurl:")[-1]  # type: ignore
    doc_url = f"{config.LIBRARY_BASE_URL}{doc_url}"
    await callback.answer("Загрузка началась...")
    async with FlibustaParser() as parser:
        download_url = await parser.get_download_url(doc_url)
        if download_url is None:
            if callback.message is not None:
                await callback.message.answer(
                    "К сожалению, не удалось получить ссылку для скачивания книги."
                )
            return
        filename = await parser.get_filename_from_metadata(download_url)
    doc = URLInputFile(url=download_url, filename=filename)
    if callback.message is not None:
        await callback.message.answer_document(document=doc)
        # Save download event to DB
        try:
            # Extract book_id from doc_url (assuming .../b/<book_id>/...)
            match = book_id_pattern.search(doc_url)
            book_id = int(match.group(1)) if match else None
            if book_id and callback.from_user:
                async with db_session() as session:
                    from flibusta_bot.db.storage.books import register_downloaded_book

                    await register_downloaded_book(
                        session,
                        user_id=callback.from_user.id,
                        book_id=book_id,
                        format=filename.split(".")[-1] if filename else None,
                    )
        except Exception as e:
            logger.warning(f"Could not save download event to DB: {e}")


@router.message(F.text)
async def search_books(message: Message):
    if message.bot is not None:
        await message.bot.send_chat_action(
            chat_id=message.chat.id, action=ChatAction.TYPING
        )
    if not message.text:
        await message.answer("Пустой запрос.")
        return
    async with FlibustaParser() as parser:
        poges, books = await parser.search_book(message.text)

    if not books:
        answer = "К сожалению, не удалось найти ни одной книги."
        await message.answer(answer)
        return

    # TODO: add pagination for one library page (50 books) - 10 books per telegram page
    books = books[:10]
    total_books = len(books)
    answer = f"Найдено {total_books} книг:\n\n"
    books_list = [str(i) for i in books]
    books_text = "\n\n".join(books_list)
    answer += books_text
    await message.answer(answer)


async def _get_book_info(book_id: int, message: Message) -> BookInfoData | None:
    is_new_book = False

    async with db_session() as session:
        book_info = await storage.books.get_book_info(session, book_id)

    if book_info is None:
        async with FlibustaParser() as parser:
            book_info = await parser.get_book_info(book_id, message.text)
            is_new_book = True

    if book_info is None:
        return None

    if is_new_book:
        async with db_session() as session:
            book_schema = BookSchema(
                id=book_info.id,
                title=book_info.title,
                description=book_info.description,
                author=book_info.author,
                author_url=book_info.author_url,
                book_url=book_info.book_url,
                hashtags=book_info.hashtags,
            )
            try:
                await create_book(session, book_schema)
            except Exception as e:
                logger.warning(f"Could not save book to DB: {e}")

    return book_info
