from aiogram import Dispatcher

__all__ = ['setup']

from . import (start, settings, help,)


def setup(dispatcher: Dispatcher, *args, **kwargs):
    for module in (start, settings, help,):
        module.setup(dispatcher, *args, **kwargs)
