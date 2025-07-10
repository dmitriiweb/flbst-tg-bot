from typing import Protocol

from aiogram.types import InlineKeyboardButton
from aiogramx import Paginator

from flibusta_bot.tg_bot.bot import dp

CANCEL_BUTTON = "❌ Отмена"

Paginator.register(dp)


class ItemListingData(Protocol):
    def __str__(self) -> str: ...
    @property
    def id(self) -> str: ...


def item_listing_kb(
    items: list[ItemListingData], callback_prefix: str = "book"
) -> Paginator:
    inline_keyboard = [
        InlineKeyboardButton(
            text=str(item),
            callback_data=f"{callback_prefix}|{item.id}",
        )
        for item in items
    ]
    # for item in items:
    #     inline_keyboard.append(
    #         [
    #             InlineKeyboardButton(
    #                 text=str(item),
    #                 callback_data=f"{callback_prefix}|{item.id}",
    #             )
    #         ]
    #     )
    # listing_kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    pg = Paginator(per_page=7, per_row=1, data=inline_keyboard)
    return pg
