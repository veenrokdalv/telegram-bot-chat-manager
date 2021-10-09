from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Message

import loggers
from app.models.telegram_chat_member import TelegramChatMember
from app.models.telegram_chat_message import TelegramChatMessage
from app.services.repo import Repo


class TelegramChatMessageMiddleware(BaseMiddleware):

    async def __call__(self, handler, event: Message, data):
        repo: Repo = data['repo']
        telegram_chat_member: TelegramChatMember = data['telegram_chat_member']

        data['telegram_chat_message'] = None

        if not telegram_chat_member:
            return await handler(event, data)

        telegram_chat_message = await repo.get_telegram_chat_message(
            message_id=event.message_id, chat_id=event.chat.id
        )

        if not telegram_chat_message:
            message_text = event.text or event.caption
            telegram_chat_message = await repo.add_telegram_chat_message(
                message_id=event.message_id, message_text=message_text, is_deleted=False,
                chat_id=telegram_chat_member.chat_id, user_id=telegram_chat_member.user_id
            )

        loggers.middlewares.debug(
            f'Сообщение чата. '
            f'[message_id:{telegram_chat_message.message_id}] [chat_id:{telegram_chat_message.chat_id}]'
        )
        data['telegram_chat_message'] = telegram_chat_message

        return await handler(event, data)


class TelegramChatEditedMessageMiddleware(BaseMiddleware):

    async def __call__(self, handler, event: Message, data):
        repo: Repo = data['repo']
        telegram_chat_message = await repo.get_telegram_chat_message(
            message_id=event.message_id, chat_id=event.chat.id
        )
        if not telegram_chat_message:
            return await handler(event, data)

        if event.text and event.text != telegram_chat_message.message_text:
            await repo.edited_text_telegram_chat_message(id=telegram_chat_message.id, message_text=event.text)
        elif event.caption and event.caption != telegram_chat_message.message_text:
            await repo.edited_text_telegram_chat_message(id=telegram_chat_message.id, message_text=event.caption)
        else:
            return await handler(event, data)

        loggers.middlewares.debug(
            f'Сообщение изменено. '
            f'[message_id:{telegram_chat_message.message_id}] [chat_id:{telegram_chat_message.chat_id}]'
        )

        telegram_chat_message = await repo.get_telegram_chat_message(
            message_id=event.message_id, chat_id=event.chat.id
        )

        data['telegram_chat_message'] = telegram_chat_message

        return await handler(event, data)


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.message.outer_middleware(TelegramChatMessageMiddleware())
    dispatcher.edited_message.outer_middleware(TelegramChatEditedMessageMiddleware())