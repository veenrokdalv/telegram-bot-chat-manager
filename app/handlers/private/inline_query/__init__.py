from aiogram import Dispatcher

__all__ = ['setup']

from . import display_my_repo


def setup(dispatcher: Dispatcher, *args, **kwags):
    for module in (display_my_repo,):
        module.setup(dispatcher, *args, **kwags)
