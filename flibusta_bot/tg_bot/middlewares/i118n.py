from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message
from fluentogram import TranslatorHub


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:  # type: ignore[override]
        hub: TranslatorHub = data.get("translator_hub")  # type: ignore
        language_code = event.from_user.language_code if event.from_user and event.from_user.language_code else "ru"
        data["i18n"] = hub.get_translator_by_locale(language_code)
        return await handler(event, data)
