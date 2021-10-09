import asyncio
import time
from typing import Iterable, Union

from aiogram import Bot
from aiogram.types import (Message, InlineKeyboardMarkup, InputMediaAudio, InputMediaDocument, InputMediaPhoto, \
                           InputMediaVideo)

import loggers


def _get_chats(chat_ids: Union[Iterable[int], str, int]) -> Iterable[int]:
    try:
        if isinstance(chat_ids, Iterable):
            chat_ids = set(chat_ids)
        else:
            chat_ids = [int(chat_ids)]
    except Exception as ex:
        raise ValueError
    return chat_ids


async def text(
        message_text: str = None,
        input_media_files: list[Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]] = None,
        **kwargs
) -> tuple[float, int]:
    """
    Sending text messages or media.
    :param message_text:
    :param input_media_files:
    :param kwargs:
    :return: Returns a tuple of two numbers - the time of sending the mailing and the number of successful messages.
    """
    assert (message_text is not None) ^ (input_media_files is not None), ValueError(
        'Pass only 1 message_text or input_media_files argument.'
    )

    bot = kwargs.get('bot', None) or Bot.get_current()
    chat_ids: Union[Iterable[int], str, int] = kwargs.get('chat_ids', [])
    parse_mode: str = kwargs.get('parse_mode', bot.parse_mode)
    disable_notification: bool = kwargs.get('disable_notification', False)
    disable_web_page_preview: bool = kwargs.get('disable_web_page_preview', False)
    markup: InlineKeyboardMarkup = kwargs.get('markup', None)
    count_successful = 0

    chat_ids = _get_chats(chat_ids)

    start_time = time.time()
    for number, chat_id in enumerate(chat_ids, start=1):
        if number % 10 == 0:
            await asyncio.sleep(0.5)
        try:
            if input_media_files and len(input_media_files) <= 10:
                await bot.send_media_group(
                    chat_id=chat_id,
                    media=input_media_files,
                    disable_notification=disable_notification,
                )
            elif message_text:
                await bot.send_message(
                    chat_id=chat_id,
                    text=message_text,
                    parse_mode=parse_mode,
                    reply_markup=markup,
                    disable_notification=disable_notification,
                    disable_web_page_preview=disable_web_page_preview
                )
            else:
                raise ValueError('Invalid message')
        except Exception as ex:
            loggers.utils.error(f'Failed send message [chat_id:{chat_id}] {ex}')
            continue
        else:
            count_successful += 1

    end_time = round(time.time() - start_time, 3)
    relation = f'{count_successful}/{len(chat_ids)}'
    loggers.utils.info(f'Sending messages completed, {relation} messages success sent. [message_text] ({end_time}s)')
    return end_time, count_successful


async def copy_message(message: Message, **kwargs) -> tuple[float, int]:
    """
    Sending copy messages.
    :param message:
    :param kwargs:
    :return: Returns a tuple of two numbers - the time of sending the mailing and the number of successful messages.
    """
    bot = kwargs.get('bot', None) or Bot.get_current()
    chat_ids: Union[Iterable[int], str, int] = kwargs.get('chat_ids', [])
    parse_mode: str = kwargs.get('parse_mode', bot.parse_mode)
    disable_notification: bool = kwargs.get('disable_notification', False)
    markup: InlineKeyboardMarkup = kwargs.get('markup', None)
    count_successful = 0

    chat_ids = _get_chats(chat_ids)

    start_time = time.time()
    for number, chat_id in enumerate(chat_ids, start=1):
        if number % 10 == 0:
            await asyncio.sleep(0.5)

        try:
            await bot.copy_message(
                chat_id=chat_id,
                from_chat_id=message.from_user.id,
                message_id=message.message_id,
                parse_mode=parse_mode,
                reply_markup=markup,
                disable_notification=disable_notification,
            )
        except Exception as ex:
            loggers.utils.error(f'Failed send message [chat_id:{chat_id}] {ex}')
            continue
        else:
            count_successful += 1

    end_time = round(time.time() - start_time, 3)
    relation = f'{count_successful}/{len(chat_ids)}'
    loggers.utils.info(f'Sending messages completed, {relation} messages success sent. [copy message] ({end_time}s)')
    return end_time, count_successful


async def forward_message(message: Message, **kwargs) -> tuple[float, int]:
    """
    Sending messages using the forwarding method.
    :param message:
    :param kwargs:
    :return: Returns a tuple of two numbers - the time of sending the mailing and the number of successful messages.
    """
    bot = kwargs.get('bot', None) or Bot.get_current()
    chat_ids: Union[Iterable[int], str, int] = kwargs.get('chat_ids', [])
    disable_notification: bool = kwargs.get('disable_notification', False)
    count_successful = 0

    chat_ids = _get_chats(chat_ids)
    start_time = time.time()
    for number, chat_id in enumerate(chat_ids, start=1):
        if number % 10 == 0:
            await asyncio.sleep(0.5)

        try:
            await bot.forward_message(
                chat_id=chat_id,
                from_chat_id=message.from_user.id,
                message_id=message.message_id,
                disable_notification=disable_notification,
            )
        except Exception as ex:
            loggers.utils.error(f'Failed send message [chat_id:{chat_id}] {ex}')
            continue
        else:
            count_successful += 1

    end_time = round(time.time() - start_time, 3)
    relation = f'{count_successful}/{len(chat_ids)}'
    loggers.utils.info(
        f'Sending messages completed, {relation} messages success sent. [forward message] ({end_time}s)')
    return end_time, count_successful
