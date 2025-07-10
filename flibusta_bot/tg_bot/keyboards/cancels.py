from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

CANCEL_BUTTON = "❌ Отмена"


def single_cansel_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=CANCEL_BUTTON)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
