from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_pagination import NavigationButtons, Paginator

from flibusta_bot.flibusta_parser import schemas
from flibusta_bot.tg_bot.bot import dp

CANCEL_BUTTON = "❌ Отмена"


def book_listing_kb(books: list[schemas.BookListingData]) -> Paginator:
    inline_keyboard = []
    for book in books:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{book.title} - {book.author}",
                    callback_data=f"book|{book.book_id}",
                )
            ]
        )

    add_kb = InlineKeyboardMarkup(
        one_time_keyboard=True,
        inline_keyboard=[
            [InlineKeyboardButton(text=CANCEL_BUTTON, callback_data="back")]
        ],
    )
    listing_kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    kb_with_pagination = Paginator(
        dp=dp,
        keyboard=listing_kb,
        page_size=6,
        nav_buttons=NavigationButtons(
            callback_prefix="call",
            back="Назад",
            next="Дальше",
            separator="|",
        ),
        additional_keyboard=add_kb,
    )
    return kb_with_pagination
