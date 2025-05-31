from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def choose_download_format_keyboard(download_urls: list[str]) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text=download_url.split("/")[-1].lower(),
            callback_data=f"download:url{download_url}",
        )
        for download_url in download_urls
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return keyboard
