from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def cancel_button(button_text: str) -> ReplyKeyboardMarkup:
    """Create a reply keyboard with one cancel button."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button_text)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
