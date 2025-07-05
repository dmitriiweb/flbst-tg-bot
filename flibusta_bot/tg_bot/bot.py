from aiogram import Bot, Dispatcher

from .. import config

assert config.TG_BOT_TOKEN, "TG_BOT_TOKEN is not set"
bot = Bot(token=config.TG_BOT_TOKEN)
dp = Dispatcher()


__all__ = ["bot", "dp"]
