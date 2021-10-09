from aiogram import Dispatcher

import loggers
from . import translate


def setup(dispatcher: Dispatcher, *args, **kwargs):
    for module in (translate, ):
        module.setup(dispatcher, *args, **kwargs)

    loggers.middlewares.debug('Setup middlewares.')
