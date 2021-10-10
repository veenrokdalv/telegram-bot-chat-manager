import asyncio
import datetime as dt

from aiogram import Dispatcher, F
from aiogram.dispatcher.filters import CommandObject
from aiogram.methods import BanChatMember
from aiogram.types import Message

from app.utils.parse.time_delta import parse_timedelta


async def ban_user_from_reply_to_message(message: Message, command: CommandObject, _):
    try:
        until_date = parse_timedelta(command.args, default=dt.timedelta(days=370))
        await BanChatMember(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            revoke_messages=True,
            until_date=until_date,
        )
        service_message = await message.reply(
            _(f'Я заблокировал пользователя на {until_date}с')
        )
    except Exception as ex:
        service_message = await message.reply(
            _('У меня не получилось применить ограничения к этому пользователю!\n'
              f'{ex}')
        )
    await asyncio.sleep(10)
    try:
        await service_message.delete()
        await message.delete()
        await message.reply_to_message.delete()
    except:
        pass


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.message.register(
        ban_user_from_reply_to_message, F.chat.type.in_(('group', 'supergroup')), F.reply_to_message,
        commands=['ban', 'b'], commands_prefix='/!', member_permissions='can_restrict_members'
    )
