import asyncio
import datetime as dt

from aiogram import F, Dispatcher
from aiogram.dispatcher.filters.command import CommandObject
from aiogram.methods import RestrictChatMember
from aiogram.types import Message, ChatPermissions

from app.utils.parse.time_delta import parse_timedelta


async def mute_user_from_reply_to_message(message: Message, command: CommandObject, _):
    try:
        until_date = parse_timedelta(command.args, default=dt.timedelta(minutes=15))
        await RestrictChatMember(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
            ),
            until_date=until_date
        )
        service_message = await message.reply(
            _(f'Я запретил писать пользователю на {until_date}с')
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
        mute_user_from_reply_to_message, F.chat.type.in_(('group', 'supergroup')), F.reply_to_message,
        commands=['mute', 'm'], commands_prefix='/!', member_permissions='can_restrict_members'
    )
