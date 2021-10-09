from aiogram.types import ReplyKeyboardMarkup


def user_keyboard(_, **kwargs) -> ReplyKeyboardMarkup:
    locale = kwargs.get('locale')
    markup: ReplyKeyboardMarkup = None
    return markup


def superuser_keyboard(_, **kwargs) -> ReplyKeyboardMarkup:
    locale = kwargs.get('locale')
    markup: ReplyKeyboardMarkup = None
    return markup
