from aiogram import BaseMiddleware, Dispatcher

from app.services.repo import Repo


class TelegramChatMiddleware(BaseMiddleware):

    async def __call__(self, handler, event, data):
        repo: Repo = data['repo']

        data['telegram_chat'] = None

        if not hasattr(event.event, 'chat'):
            return await handler(event, data)

        telegram_chat = await repo.get_telegram_chat(id=event.event.chat.id)
        if not telegram_chat:
            telegram_chat = await repo.add_telegram_chat(id=event.event.chat.id)

        data['telegram_chat'] = telegram_chat

        return await handler(event, data)


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.update.outer_middleware(TelegramChatMiddleware())
