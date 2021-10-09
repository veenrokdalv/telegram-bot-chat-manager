from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated, InlineQuery


class ChatTypeFilter(BaseFilter):
    chat_type: str

    async def __call__(self, obj: Union[Message, CallbackQuery, InlineQuery, ChatMemberUpdated]):
        if isinstance(obj, Message):
            obj = obj.chat
        elif isinstance(obj, InlineQuery):
            return obj.chat_type in self.chat_type
        elif isinstance(obj, CallbackQuery):
            obj = obj.message.chat
        elif isinstance(obj, ChatMemberUpdated):
            obj = obj.chat
        else:
            return False
        return obj.type in self.chat_type


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.message.bind_filter(ChatTypeFilter)
    dispatcher.callback_query.bind_filter(ChatTypeFilter)
    dispatcher.inline_query.bind_filter(ChatTypeFilter)
    dispatcher.chat_member.bind_filter(ChatTypeFilter)
