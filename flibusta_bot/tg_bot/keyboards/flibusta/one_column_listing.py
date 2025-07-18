from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def one_column_listing(
    *buttons: str,
) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[[KeyboardButton(text=button)] for button in buttons],
    )
