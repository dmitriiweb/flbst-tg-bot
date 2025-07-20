from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from flibusta_bot.parsers.gutenberg import schemas


def download_formats_kb(
    download_datas: list[schemas.DownloadUrlData], i18n: TranslatorRunner
) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=i.title, callback_data=f"gdb|{i.download_file_format}"
            )
        ]
        for i in download_datas
    ]
    inline_keyboard.append(
        [InlineKeyboardButton(text=i18n.cancel.button(), callback_data="back")]
    )
    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return kb
