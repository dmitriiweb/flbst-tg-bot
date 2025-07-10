from aiogram import Bot, Dispatcher
from fluentogram import FluentTranslator, TranslatorHub
from fluentogram.translator import FluentBundle

from .. import config

LOCALES_DIR = config.BASE_DIR / "locales"
RU_LOCALE_FILE = LOCALES_DIR / "ru" / "LC_MESSAGES" / "tg-bot.ftl"

available_locales = ["en", "ru"]
translator_hub = TranslatorHub(
    {
        "ru": ("ru",),
        "en": ("ru",),
    },
    [
        FluentTranslator(
            "ru",
            translator=FluentBundle.from_files("ru", filenames=[RU_LOCALE_FILE]),
        ),
        FluentTranslator(
            "en",
            translator=FluentBundle.from_files("ru", filenames=[RU_LOCALE_FILE]),
        ),
    ],
)

assert config.TG_BOT_TOKEN, "TG_BOT_TOKEN is not set"
bot = Bot(token=config.TG_BOT_TOKEN)
dp = Dispatcher(translator_hub=translator_hub)


__all__ = ["bot", "dp"]
