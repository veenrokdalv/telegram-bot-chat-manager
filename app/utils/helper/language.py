from aiogram.utils.helper import Helper, Item, HelperMode


class LanguageCodeType(Helper):
    """Класс языковых кодов"""
    mode = HelperMode.lowercase

    RU = Item()
    EN = Item()
    BE = Item()
    UK = Item()
