from aiogram import Bot, Dispatcher
from fluentogram import FluentTranslator, TranslatorHub
from fluentogram.translator import FluentBundle

from .. import config

LOCALES_DIR = config.BASE_DIR / "locales"
RU_LOCALE_FILE = LOCALES_DIR / "ru" / "LC_MESSAGES" / "tg-bot.ftl"
EN_LOCALE_FILE = LOCALES_DIR / "en" / "LC_MESSAGES" / "tg-bot.ftl"

available_locales = [
    "ar",  # Arabic
    "az",  # Azerbaijani
    "bg",  # Bulgarian
    "de",  # German
    "en",  # English
    "es",  # Spanish
    "fa",  # Persian
    "fi",  # Finnish
    "fr",  # French
    "he",  # Hebrew
    "hi",  # Hindi
    "id",  # Indonesian
    "it",  # Italian
    "ja",  # Japanese
    "kk",  # Kazakh
    "ko",  # Korean
    "mn",  # Mongolian
    "nl",  # Dutch
    "pl",  # Polish
    "pt",  # Portuguese
    "ro",  # Romanian
    "ru",  # Russian
    "tg",  # Tajik
    "th",  # Thai
    "tr",  # Turkish
    "uk",  # Ukrainian
    "uz",  # Uzbek
    "zh-hans",  # Chinese Simplified
    "zh-hant",  # Chinese Traditional
]
translator_hub = TranslatorHub(
    {
        "ru": ("ru",),
        "en": ("en",),
    },
    [
        FluentTranslator(
            "ru",
            translator=FluentBundle.from_files("ru", filenames=[RU_LOCALE_FILE]),
        ),
        FluentTranslator(
            "en",
            translator=FluentBundle.from_files("en", filenames=[EN_LOCALE_FILE]),
        ),
    ],
)

assert config.TG_BOT_TOKEN, "TG_BOT_TOKEN is not set"
bot = Bot(token=config.TG_BOT_TOKEN)
dp = Dispatcher(translator_hub=translator_hub)


__all__ = ["bot", "dp"]
