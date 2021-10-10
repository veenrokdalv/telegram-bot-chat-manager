from aiogram import Dispatcher

import loggers
from . import (translated_inline_query_text, translated_message_text, has_permissions, )


def setup(dispatcher: Dispatcher):
    for module in (translated_inline_query_text, translated_message_text, has_permissions, ):
        module.setup(dispatcher)
    loggers.filters.debug('Setup filters.')
