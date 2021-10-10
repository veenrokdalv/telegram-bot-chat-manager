from aiogram import Dispatcher

import loggers
from . import (translate, telegram_user, telegram_chat, telegram_chat_member, telegram_chat_message,
               flood_control_in_group)


def setup(dispatcher: Dispatcher, *args, **kwargs):
    for module in (translate, telegram_user, telegram_chat, telegram_chat_member, telegram_chat_message,
                   flood_control_in_group):
        module.setup(dispatcher, *args, **kwargs)

    loggers.middlewares.debug('Setup middlewares.')
