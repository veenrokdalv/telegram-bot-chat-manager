from aiogram import Bot, Dispatcher, F

from aiogram.types import Update, ChatJoinRequest

import loggers


async def join_member(chat_join_request: ChatJoinRequest, bot: Bot):
    loggers.handlers.debug(chat_join_request)
    await chat_join_request.approve()


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.chat_join_request.register(join_member, F.chat.type.in_(('channel',)))
