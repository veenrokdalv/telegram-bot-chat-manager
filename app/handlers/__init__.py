from aiogram import Dispatcher

import loggers
from . import private

__all__ = ['setup']


def setup(dispatcher: Dispatcher):
    for module in (private, ):
        module.setup(dispatcher)

    loggers.handlers.debug('Setup handlers.')
