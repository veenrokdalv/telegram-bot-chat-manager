from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Update

from app.models.telegram_chat import TelegramChat
from app.models.telegram_user import TelegramUser


class TelegramChatMemberMiddleware(BaseMiddleware):

    async def __call__(self, handler, event: Update, data):
        repo: Repo = data['repo']
        telegram_user: TelegramUser = data['telegram_user']
        telegram_chat: TelegramChat = data['telegram_chat']

        data['telegram_chat_member'] = None

        if not hasattr(event.event, 'chat') and not (telegram_user or telegram_chat):
            return await handler(event, data)

        telegram_chat_member = await repo.get_telegram_chat_member(
            chat_id=telegram_chat.id, user_id=telegram_user.id
        )

        if not telegram_chat_member:
            telegram_chat_member = await repo.add_telegram_chat_member(
                chat_id=telegram_chat.id, user_id=telegram_user.id
            )

        data['telegram_chat_member'] = telegram_chat_member

        return await handler(event, data)


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.update.outer_middleware(TelegramChatMemberMiddleware())
