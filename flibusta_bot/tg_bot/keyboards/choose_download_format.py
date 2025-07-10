from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger


def choose_download_format_keyboard(download_urls: list[str]) -> InlineKeyboardMarkup:
    logger.debug(f"{download_urls=}")
    buttons = []
    for download_url in download_urls:
        file_format = download_url.split("/")[-1].lower()
        logger.debug(f"{file_format=}")
        button = InlineKeyboardButton(
            text=file_format if "download" not in file_format else "Скачать",
            callback_data=f"downloadurl|{download_url}",
        )
        buttons.append(button)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    logger.debug(f"{keyboard=}")
    return keyboard
