from aiogram import Dispatcher, html

__all__ = ['setup']

from aiogram.types import Message
from aiogram import F
import loggers
from app.utils.helper import formatting


async def info_chat_member_from_reply_message(message: Message, _):
    await message.reply(
        text=_(
            'Информация о пользователе.\n'
            '<b>ID:</> <i><code>{member_id}</></>\n'
            '<b>Имя:</> <i>{member_fullname}</>\n'
            '<b>Username:</> <i>{member_username}</>\n'
            '<b>Репутация:</> <i>Soon...</>\n'
        ).format(
            member_id=message.reply_to_message.from_user.id,
            member_fullname=html.link(message.reply_to_message.from_user.full_name,
                                      f'tg://user?id={message.reply_to_message.from_user.id}'),
            member_username=formatting.username(message.reply_to_message.from_user, default=_('Отсутсвует'))
        )
    )


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.message.register(
        info_chat_member_from_reply_message, F.chat.type.in_(('group', 'supergroup')), F.reply_to_message,
        commands=['info'], commands_prefix='/!',
    )
