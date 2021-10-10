from aiogram import Dispatcher

import loggers
from . import (private, group)

__all__ = ['setup']


def setup(dispatcher: Dispatcher):
    for module in (private, group):
        module.setup(dispatcher)

    loggers.handlers.debug('Setup handlers.')
