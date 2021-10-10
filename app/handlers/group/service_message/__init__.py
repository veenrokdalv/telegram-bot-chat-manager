from aiogram import Dispatcher
from . import (left_member, join_member)
__all__ = ['setup']


def setup(dispatcher: Dispatcher, *args, **kwargs):
    for module in (left_member, join_member):
        module.setup(dispatcher, *args, **kwargs)
