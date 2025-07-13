from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def choose_download_format_keyboard(download_urls: list[str], download_button_text: str) -> InlineKeyboardMarkup:
    buttons = []
    for download_url in download_urls:
        file_format = download_url.split("/")[-1].lower()
        button = InlineKeyboardButton(
            text=file_format if "download" not in file_format else download_button_text,
            callback_data=f"downloadurl|{download_url}",
        )
        buttons.append(button)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return keyboard
