from aiogram import Dispatcher, html
from aiogram import F
from aiogram.types import Message
from aiogram.utils.i18n import I18n


async def start(message: Message, _: I18n.gettext):
    await message.answer(
        text=_(f'Hi! {html.link("My repo", "https://github.com/Robot-meow/aiogram-template-bot")}')
    )


def setup(dispatcher: Dispatcher):
    dispatcher.message.register(
        start, F.chat.type.in_(('private',)),  commands='start',
    )
