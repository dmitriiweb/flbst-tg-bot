from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def single_cansel_kb(cancel_button: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cancel_button)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
