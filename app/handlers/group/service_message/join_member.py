import asyncio

from aiogram import Dispatcher, html
from aiogram.types import Message, ContentType


async def join_member(message: Message, _):
    await message.delete()
    service_message = await message.answer(
        _(
            "<b>Добро пожаловать</>, <i>{member_full_name}</>"
        ).format(
            member_full_name=html.link(message.from_user.full_name, f'tg://user?id={message.from_user.id}')
        )
    )
    await asyncio.sleep(15)
    await service_message.delete()


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.message.register(
        join_member,
        content_types=ContentType.NEW_CHAT_MEMBERS
    )
