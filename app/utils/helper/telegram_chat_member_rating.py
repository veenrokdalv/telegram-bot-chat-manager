from aiogram.utils.helper import Helper, HelperMode, Item


class TelegramChatMemberRatingStatus(Helper):
    mode = HelperMode.CamelCase
    ACTIVE = Item()
    REVOKED = Item()