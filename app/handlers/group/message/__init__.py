from aiogram import Dispatcher

from . import commands, recognize_video_note, recognize_voice

__all__ = ['setup']


def setup(dispatcher: Dispatcher, *args, **kwargs):
    for module in (commands, recognize_video_note, recognize_voice):
        module.setup(dispatcher, *args, **kwargs)
