from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from flibusta_bot.parsers.gutenberg import schemas


def book_listing_kb(
    books: list[schemas.BookListingData],
    prev_index: str | None,
    next_index: str | None,
    i18n: TranslatorRunner,
) -> InlineKeyboardMarkup:
    books_buttons = [
        [InlineKeyboardButton(text=i.title, callback_data=f"book|{i.book_id}")]
        for i in books
    ]
    if prev_index:
        books_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.gutenberg.listing.previous(),
                    callback_data=f"nav_button|{prev_index}",
                )
            ]
        )
    if next_index:
        books_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.gutenberg.listing.next(),
                    callback_data=f"nav_button|{next_index}",
                )
            ]
        )
    books_buttons.append(
        [InlineKeyboardButton(text=i18n.cancel.button(), callback_data="back")]
    )
    return InlineKeyboardMarkup(inline_keyboard=books_buttons)
