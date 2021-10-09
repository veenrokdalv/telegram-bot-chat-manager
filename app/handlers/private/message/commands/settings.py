import datetime as dt
from zoneinfo import ZoneInfo

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.i18n import I18n

import settings
from app.utils.bot.send_keyboards import get_main_keyboard
from app.utils.helper import formatting

__all__ = ['setup']


async def settings_menu(message: Message, _: I18n.gettext):
    await message.answer(
        reply_markup=get_main_keyboard(_, message.from_user),
        text=_(
            'Menu settings\n\n'
            'Current time: {current_datetime}\n'
            'Timezone: "{user_timezone}"\n'
            'Locale: {user_locale}'
        ).format(
            current_datetime=(dt.datetime.now(ZoneInfo(settings.DEFAULT_TIMEZONE))).strftime('%Y-%m-%d %H:%M:%S'),
            user_timezone=settings.DEFAULT_TIMEZONE,
            user_locale=f'{settings.DEFAULT_LOCALE} '
                        f'{formatting.country_flag(settings.DEFAULT_LOCALE)} '
                        f'{formatting.title_country(settings.DEFAULT_LOCALE)}',
        )
    )


def setup(dispatcher: Dispatcher):
    dispatcher.message.register(
        settings_menu, state=None, commands=['settings'], chat_type='private',
    )
