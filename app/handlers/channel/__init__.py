from aiogram import Dispatcher

import loggers
from . import new_member

__all__ = ['setup']


def setup(dispatcher: Dispatcher):
    for module in (new_member, ):
        module.setup(dispatcher)
