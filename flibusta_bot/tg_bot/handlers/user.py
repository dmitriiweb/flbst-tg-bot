import re
from dataclasses import dataclass

from aiogram import F, Router
from aiogram.enums import ChatAction, ChatType, ParseMode
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    URLInputFile,
)
from loguru import logger

from flibusta_bot import config
from flibusta_bot.flibusta_parser import App as FlibustaParser
from flibusta_bot.flibusta_parser import schemas
from flibusta_bot.tg_bot.keyboards import choose_download_format_keyboard

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)

book_id_pattern = re.compile(r"/b/(\d+)")


@dataclass
class FileUrl:
    download_url: str
    filename: str
    format: str
    callback_data: str


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


@router.message(F.text.startswith("/b"), F.text.endswith(config.TG_BOT_NAME))
async def book_info(message: Message):
    try:
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

        logger.info(
            f"{book_info.id=} {book_info.title=} {book_info.author=} {book_info.book_url=}"
        )
        download_urls = [i.url for i in book_info.download_urls]
        reply_markup = choose_download_format_keyboard(download_urls=download_urls)
        await message.answer(
            book_info.to_telegram_message(),
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
        )
    except Exception as e:
        logger.error(f"book_info error: {e}")
        try:
            await message.answer("Извините, произошла ошибка. Попробуйте позже.")
        except Exception:
            pass


@router.callback_query(F.data.startswith("downloadurl:"), F.data.endswith("download"))
async def download_book_format(callback: CallbackQuery):
    try:
        if callback.data is None:
            return None
        file_url = await _get_file_url(callback.data, callback)
        if callback.message is None:
            return None

        if callback.message and callback.bot is not None:
            await callback.bot.send_chat_action(
                chat_id=callback.message.chat.id, action=ChatAction.TYPING
            )
        if file_url is None:
            await callback.message.answer(
                "К сожалению, не удалось получить ссылку для скачивания книги."
            )
            return
        answer = f"Для данной книги доступен только один формат: {file_url.format}"
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Скачать {file_url.format.lower()}",
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
                await callback.message.answer(
                    "Извините, произошла ошибка. Попробуйте позже."
                )
            except Exception:
                pass


@router.callback_query(F.data.startswith("downloadurl:"))
async def download_book(callback: CallbackQuery):
    try:
        callback_data = callback.data
        if callback_data is None:
            return
        if callback.message is None:
            return
        if callback.message and callback.bot is not None:
            await callback.bot.send_chat_action(
                chat_id=callback.message.chat.id, action=ChatAction.TYPING
            )
        if "downloads" in callback_data:
            callback_data = callback_data.replace("downloads", "download")
        file_url = await _get_file_url(callback_data, callback)
        if file_url is None:
            await callback.message.answer(
                "К сожалению, не удалось получить ссылку для скачивания книги."
            )
            return
        logger.info(f"{file_url.filename=} {file_url.download_url=}")
        await callback.answer("Загрузка началась...")
        doc = URLInputFile(url=file_url.download_url, filename=file_url.filename)
        if callback.message is not None:
            await callback.message.answer_document(document=doc)
    except Exception as e:
        logger.error(f"download_book error: {e}")
        if callback.message is not None:
            try:
                await callback.message.answer(
                    "Извините, произошла ошибка. Попробуйте позже."
                )
            except Exception:
                pass


@router.message(F.text)
async def search_books(message: Message):
    try:
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
    except Exception as e:
        logger.error(f"search_books error: {e}")
        try:
            await message.answer("Извините, произошла ошибка. Попробуйте позже.")
        except Exception:
            pass


async def _get_file_url(callback_data: str, callback: CallbackQuery) -> FileUrl | None:
    doc_url = callback_data.split("downloadurl:")[-1]  # type: ignore
    doc_url = f"{config.LIBRARY_BASE_URL}{doc_url}"
    async with FlibustaParser() as parser:
        download_url = await parser.get_download_url(doc_url)
        if download_url is None:
            if callback.message is not None:
                await callback.message.answer(
                    "К сожалению, не удалось получить ссылку для скачивания книги."
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


async def _get_book_info(book_id: int, message: Message) -> schemas.BookInfoData | None:
    try:
        async with FlibustaParser() as parser:
            book_info = await parser.get_book_info(book_id, message.text)
        return book_info
    except Exception as e:
        logger.error(f"_get_book_info error: {e}")
        return None
