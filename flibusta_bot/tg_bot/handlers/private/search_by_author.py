import re
from dataclasses import dataclass

from aiogram import F, Router
from aiogram.enums import ChatAction, ChatType, ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    URLInputFile,
)
from loguru import logger

from flibusta_bot import config
from flibusta_bot.flibusta_parser import App as FlibustaParser
from flibusta_bot.flibusta_parser import schemas
from flibusta_bot.tg_bot import states as bot_states
from flibusta_bot.tg_bot.keyboards import cancels as cancels_keyboard
from flibusta_bot.tg_bot.keyboards import choose_download_format_keyboard
from flibusta_bot.tg_bot.keyboards import start as start_keyboard

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)


