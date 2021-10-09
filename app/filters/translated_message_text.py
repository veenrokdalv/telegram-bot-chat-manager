from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

from settings import DEFAULT_LOCALE


class TranslatedTextFilter(BaseFilter):
    message_text: str

    async def __call__(self, msg: Union[Message], _):
        return _(msg.text, locale=DEFAULT_LOCALE) == _(self.message_text, locale=DEFAULT_LOCALE)


def setup(dispatcher: Dispatcher):
    dispatcher.message.bind_filter(TranslatedTextFilter)
