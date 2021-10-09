from aiogram import Dispatcher

from . import inline_query, message,  callback_query


def setup(dispatcher: Dispatcher):
    for module in (inline_query, message,  callback_query):
        module.setup(dispatcher)
