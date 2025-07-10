from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_start_keyboard(
    search_by_title_button: str, search_by_author_button: str
) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text=search_by_title_button)],
            [KeyboardButton(text=search_by_author_button)],
        ],
    )
