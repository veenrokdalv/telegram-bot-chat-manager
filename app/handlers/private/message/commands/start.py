from aiogram import Dispatcher, html
from aiogram import F
from aiogram.types import Message
from aiogram.utils.i18n import I18n

import loggers


async def start_user(message: Message, _: I18n.gettext):
    await message.answer(
        text=_(f'Hi! {html.link("My repo", "https://github.com/Robot-meow/aiogram-template-bot")}')
    )


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.message.register(
        start_user, F.chat.type.in_(('private',)), commands=('start',),
    )
