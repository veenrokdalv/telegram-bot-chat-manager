from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Update

from app.services.repo import Repo


class TelegramUserMiddleware(BaseMiddleware):

    async def __call__(self, handler, event: Update, data):
        repo: Repo = data['repo']

        if not hasattr(event.event, 'from_user'):
            return await handler(event, data)

        telegram_user = await repo.get_telegram_user(id=event.event.from_user.id)
        if not telegram_user:
            telegram_user = await repo.add_telegram_user(id=event.event.from_user.id)

        data['telegram_user'] = telegram_user

        return await handler(event, data)


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.update.outer_middleware(TelegramUserMiddleware())