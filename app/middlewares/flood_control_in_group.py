import datetime as dt

from aiogram import BaseMiddleware, Dispatcher
from aiogram.methods import GetChatMember, RestrictChatMember
from aiogram.types import Message, ChatPermissions

import loggers
from app.models.telegram_chat import TelegramChat
from app.models.telegram_chat_member import TelegramChatMember
from app.services.repo import Repo


class FloodControlInGroupWiddleware(BaseMiddleware):

    async def __call__(self, handler, event: Message, data):
        if event.chat.type not in ('group', 'supergroup'):
            return await handler(event, data)

        repo: Repo = data['repo']
        _: Repo = data['_']
        telegram_chat: TelegramChat = data['telegram_chat']
        telegram_chat_member: TelegramChatMember = data['telegram_chat_member']

        if not telegram_chat.use_flood_control:
            return await handler(event, data)

        count_messages = await repo.get_telegram_chat_messages_from_chat_member(
            user_id=telegram_chat_member.user_id, chat_id=telegram_chat_member.chat_id,
            datetime_interval=dt.timedelta(seconds=7), as_int=True,
        )
        loggers.middlewares.debug(f'Count messages - {count_messages}')
        if count_messages >= 7:
            member = await GetChatMember(chat_id=telegram_chat_member.chat_id, user_id=telegram_chat_member.user_id)
            if member.status in ['creator', 'administrator']:
                return await handler(event, data)
            await RestrictChatMember(
                chat_id=telegram_chat_member.chat_id,
                user_id=telegram_chat_member.user_id,
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                ),
                until_date=dt.timedelta(minutes=1)
            )

        return await handler(event, data)


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.message.outer_middleware(FloodControlInGroupWiddleware())
