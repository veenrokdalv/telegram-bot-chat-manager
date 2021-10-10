import asyncio

from aiogram import Dispatcher, html
from aiogram.types import Message, ContentType


async def left_member(message: Message):
    await message.delete()


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.message.register(
        left_member, content_types=ContentType.LEFT_CHAT_MEMBER
    )
