from aiogram import Dispatcher

from . import commands

__all__ = ['setup']


def setup(dispatcher: Dispatcher, *args, **kwargs):
    for module in (commands, ):
        module.setup(dispatcher, *args, **kwargs)
