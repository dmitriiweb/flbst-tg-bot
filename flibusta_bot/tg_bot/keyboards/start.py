from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

SEARCH_BY_TITLE_BUTTON = "📚 Поиск по названию"
SEARCH_BY_AUTHOR_BUTTON = "👤 Поиск по автору"


def get_start_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text=SEARCH_BY_TITLE_BUTTON)],
            [KeyboardButton(text=SEARCH_BY_AUTHOR_BUTTON)],
        ],
    )
