from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, URLInputFile
from fluentogram import TranslatorRunner  # type: ignore
from loguru import logger

from flibusta_bot.parsers.gutenberg.app import App as GutenbergParser
from flibusta_bot.tg_bot.filters.i18n_filter import I18nFilter
from flibusta_bot.tg_bot.keyboards import gutenberg as kbs
from flibusta_bot.tg_bot.keyboards.flibusta import one_column_listing
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
    kb = kbs.book_listing_kb(books, prev_index, next_index, i18n)
    await callback.message.answer(
        i18n.gutenberg.listing.book.title(query=user_query), reply_markup=kb
    )


@router.callback_query(
    StateFilter(GutenbergStartStates.search_query), F.data.startswith("book")
)
async def book_info(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner, **data
):
    book_id = callback.data.split("|")[-1]
    async with GutenbergParser() as parser:
        book_info = await parser.get_book_info(book_id)
    if book_info is None:
        return
    answer = f"{book_info.title}\n\n{book_info.author}\n\n{book_info.description}"[
        :4096
    ]
    kb = kbs.download_formats_kb(book_info.download_urls, i18n)
    await state.update_data(book_id=book_id)
    await state.update_data(book_title=book_info.title)
    await callback.message.answer(answer, reply_markup=kb)
    await state.set_state(GutenbergStartStates.download_book)


@router.callback_query(
    StateFilter(GutenbergStartStates.download_book), F.data.startswith("gdb")
)
async def download_book(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner, **data
):
    download_format = callback.data.split("|")[-1]
    state_data = await state.get_data()
    book_id = state_data.get("book_id")
    book_title = state_data.get("book_title")
    await callback.answer(i18n.search.by.title.download.started())
    async with GutenbergParser() as parser:
        book = await parser.download_book(book_id, download_format)
    if book is None:
        return

    doc = URLInputFile(
        url=parser.get_download_url(book_id, download_format),
        filename=f"{book_title.lower().replace(' ', '_')}.{download_format.rstrip('.images')}",
    )
    kb = one_column_listing(
        i18n.start.choose.library.flibusta(),
        i18n.start.choose.library.gutenberg(),
    )
    await callback.message.answer_document(document=doc, reply_markup=kb)
    await state.clear()
