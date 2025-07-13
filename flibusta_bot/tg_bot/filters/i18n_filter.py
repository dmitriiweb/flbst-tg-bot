from aiogram.filters import Filter
from aiogram.types import Message, User
from fluentogram import TranslatorHub


class I18nFilter(Filter):
    def __init__(self, expected_text: str):
        self.expected_text = expected_text

    async def __call__(self, message: Message, event_from_user: User, **data) -> bool:
        hub: TranslatorHub = data.get("translator_hub")
        translator = hub.get_translator_by_locale("en")
        tr_text = translator.get(self.expected_text)
        message_text = message.text
        result = tr_text == message_text
        return result
