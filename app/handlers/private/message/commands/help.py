from aiogram import Dispatcher, html
from aiogram.types import Message
from aiogram.utils.i18n import I18n

from app.utils.bot.send_keyboards import get_main_keyboard

__all__ = ['setup']


async def help_menu(message: Message, _: I18n.gettext):
    await message.answer(
        reply_markup=get_main_keyboard(_, message.from_user),
        text=_(f'{html.link("My repo", "https://github.com/Robot-meow/aiogram-template-bot")}')
    )


def setup(dispatcher: Dispatcher):
    dispatcher.message.register(
        help_menu, state=None, commands=['help'], chat_type='private',
    )
