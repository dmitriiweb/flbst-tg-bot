from aiogram import Bot, Dispatcher

from .. import config
from .translator import translator_hub

assert config.TG_BOT_TOKEN, "TG_BOT_TOKEN is not set"
bot = Bot(token=config.TG_BOT_TOKEN)
dp = Dispatcher(translator_hub=translator_hub)


__all__ = ["bot", "dp"]
