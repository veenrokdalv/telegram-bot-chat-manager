from aiogram import Dispatcher
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.i18n import I18n

__all__ = ['setup']


async def display_my_repo(query: InlineQuery, _: I18n.gettext):
    return await query.answer(
        results=[
            InlineQueryResultArticle(
                id='0',
                thumb_url='https://telegra.ph/file/1afbefdd3b604c99d92f6.jpg',
                title=_('Link to my repo!'),
                description=_('Click on the photo to go!'),
                url='https://github.com/Robot-meow/aiogram-template-bot',
                input_message_content=InputTextMessageContent(
                    message_text=_('Link my repo - https://github.com/Robot-meow/aiogram-template-bot')
                ),
            )
        ],
        cache_time=3600,
    )


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.inline_query.register(display_my_repo, chat_type='private')
