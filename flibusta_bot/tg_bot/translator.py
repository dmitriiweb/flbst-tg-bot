from fluentogram import FluentTranslator, TranslatorHub  # type: ignore
from fluentogram.translator import FluentBundle  # type: ignore

from flibusta_bot import config

LOCALES_DIR = config.BASE_DIR / "locales"
# RU_LOCALE_FILE = LOCALES_DIR / "ru" / "LC_MESSAGES" / "tg-bot.ftl"
# EN_LOCALE_FILE = LOCALES_DIR / "en" / "LC_MESSAGES" / "tg-bot.ftl"

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
    {locale: (locale,) for locale in available_locales},
    [
        FluentTranslator(
            locale,
            translator=FluentBundle.from_files(
                locale, filenames=[LOCALES_DIR / locale / "LC_MESSAGES" / "tg-bot.ftl"]
            ),
        )
        for locale in available_locales
    ],
)
