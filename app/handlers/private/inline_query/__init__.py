from aiogram import Dispatcher

__all__ = ['setup']



def setup(dispatcher: Dispatcher, *args, **kwags):
    for module in ():
        module.setup(dispatcher, *args, **kwags)
