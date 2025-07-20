from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from fluentogram import TranslatorHub  # type: ignore


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable, event: TelegramObject, data: dict
    ) -> Any:
        hub: TranslatorHub = data.get("translator_hub")  # type: ignore
        language_code = (
            event.from_user.language_code  # type: ignore[attr-defined]
            if hasattr(event, "from_user") and event.from_user
            else "en"  # type: ignore[attr-defined]
        )
        data["i18n"] = hub.get_translator_by_locale(language_code)
        return await handler(event, data)
