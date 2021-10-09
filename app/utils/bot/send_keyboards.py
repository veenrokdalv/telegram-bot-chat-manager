from typing import Optional

from aiogram import Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup

import settings
from app.keyboards import reply


async def send_main_keyboard(_, user, state: FSMContext = None, **kwargs):
    bot: Bot = kwargs.get('bot', Bot.get_current())

    if isinstance(state, FSMContext):
        await state.clear()

    keyboard = get_main_keyboard(_, user, locale=kwargs.get('locale'))

    text = _('Вы перемещены на главное меню', locale=kwargs.get('locale'))

    await bot.send_message(
        text=text,
        reply_markup=keyboard
    )


def get_main_keyboard(_, user, **kwargs) -> Optional[ReplyKeyboardMarkup]:
    if user.id in settings.SUPERUSERS_TELEGRAM_ID:
        keyboard = reply.start.superuser_keyboard(_, locale=kwargs.get('locale'))
    else:
        keyboard = reply.start.user_keyboard(_, locale=kwargs.get('locale'))

    return keyboard
