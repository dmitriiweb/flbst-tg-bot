from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from flibusta_bot.parsers.gutenberg import schemas


def download_formats_kb(
    download_datas: list[schemas.DownloadUrlData],
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i.title, callback_data=f"gdb|{i.download_file_format}"
                )
            ]
            for i in download_datas
        ]
    )
    return kb
