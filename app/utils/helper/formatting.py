from typing import Union

from aiogram.types import User

from app.utils.helper.language import LanguageCodeType


def username(user_username: Union[str, User], default: str = 'Not user_username') -> str:
    """Форматирует user_username"""
    if isinstance(user_username, User):
        user_username = user_username.username

    if str(user_username) == 'None':
        user_username = default
    else:
        user_username = '@' + user_username

    return user_username


def title_country(language_code: str) -> str:
    """Возвращает название страны страны"""
    if language_code == LanguageCodeType.EN:
        return 'English'
    if language_code == LanguageCodeType.RU:
        return 'Русский'
    if language_code == LanguageCodeType.BE:
        return 'Беларусь'
    if language_code == LanguageCodeType.UK:
        return 'Україна'

    raise ValueError


def country_flag(language_code: str) -> str:
    """Возвращает название страны страны"""
    if language_code == LanguageCodeType.EN:
        return '🇬🇧'
    if language_code == LanguageCodeType.RU:
        return '🇷🇺'
    if language_code == LanguageCodeType.BE:
        return '🇧🇾'
    if language_code == LanguageCodeType.UK:
        return '🇺🇦'

    raise ValueError
