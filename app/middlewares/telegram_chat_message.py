import re

from aiogram import BaseMiddleware, Dispatcher, Bot
from aiogram.methods import GetChatMember
from aiogram.types import Message

import loggers
from app.models.telegram_chat import TelegramChat
from app.models.telegram_chat_member import TelegramChatMember
from app.models.telegram_chat_message import TelegramChatMessage
from app.services.repo import Repo
from app.utils.helper.telegram_chat_member_rating import TelegramChatMemberRatingStatus


class TelegramChatMessageMiddleware(BaseMiddleware):

    async def __call__(self, handler, event: Message, data):
        repo: Repo = data['repo']
        telegram_chat: TelegramChat = data['telegram_chat']
        telegram_chat_member: TelegramChatMember = data['telegram_chat_member']

        data['telegram_chat_message'] = None

        if not telegram_chat_member:
            return await handler(event, data)

        telegram_chat_message = await repo.get_telegram_chat_message(
            message_id=event.message_id, chat_id=event.chat.id
        )

        if not telegram_chat_message:
            message_text = event.text or event.caption
            telegram_chat_message = await repo.add_telegram_chat_message(
                message_id=event.message_id, message_text=message_text, is_deleted=False,
                chat_id=telegram_chat_member.chat_id, user_id=telegram_chat_member.user_id
            )

        data['telegram_chat_message'] = telegram_chat_message

        try:
            await self.message_photo_trottled(message=event, data=data)
            await self.message_video_trottled(message=event, data=data)
            await self.message_document_trottled(message=event, data=data)
            await self.message_via_bot_trottled(message=event, data=data)
            await self.forward_message_trottled(message=event, data=data)
            await self.message_link_trottled(message=event, data=data)
            await self.message_mention_bot_trottled(message=event, data=data)
        except Exception as ex:
            loggers.middlewares.error(ex)

        return await handler(event, data)

    async def message_photo_trottled(self, message: Message, data: dict):
        telegram_chat: TelegramChat = data['telegram_chat']
        telegram_chat_message: TelegramChatMessage = data['telegram_chat_message']
        telegram_chat_member = data['telegram_chat_member']
        bot: Bot = data['bot']

        if not telegram_chat.members_can_send_photo and message.photo:
            member = await GetChatMember(chat_id=telegram_chat_message.chat_id, user_id=telegram_chat_message.user_id)
            if member.status in ['creator', 'administrator']:
                return False

            try:
                await bot.delete_message(chat_id=telegram_chat_message.chat_id,
                                         message_id=telegram_chat_message.message_id, )
                await repo.deleted_telegram_chat_message(id=telegram_chat_message.id)
                await repo.add_telegram_chat_member_rating(
                    from_chat_member_id=None, in_chat_member_id=telegram_chat_member.id, value=-0.1,
                    status=TelegramChatMemberRatingStatus.ACTIVE
                )
            except:
                pass

    async def message_video_trottled(self, message: Message, data: dict):
        telegram_chat: TelegramChat = data['telegram_chat']
        telegram_chat_message = data['telegram_chat_message']
        telegram_chat_member = data['telegram_chat_member']
        bot: Bot = data['bot']

        if not telegram_chat.members_can_send_video and message.video:
            member = await GetChatMember(chat_id=telegram_chat_message.chat_id, user_id=telegram_chat_message.user_id)
            if member.status in ['creator', 'administrator']:
                return False

            try:
                await bot.delete_message(chat_id=telegram_chat_message.chat_id,
                                         message_id=telegram_chat_message.message_id, )
                await repo.deleted_telegram_chat_message(id=telegram_chat_message.id)
                await repo.add_telegram_chat_member_rating(
                    from_chat_member_id=None, in_chat_member_id=telegram_chat_member.id, value=-0.1,
                    status=TelegramChatMemberRatingStatus.ACTIVE
                )
            except:
                pass

    async def message_document_trottled(self, message: Message, data: dict):
        telegram_chat: TelegramChat = data['telegram_chat']
        telegram_chat_message = data['telegram_chat_message']
        telegram_chat_member = data['telegram_chat_member']
        bot: Bot = data['bot']

        if not telegram_chat.members_can_send_document and message.document:
            member = await GetChatMember(chat_id=telegram_chat_message.chat_id, user_id=telegram_chat_message.user_id)
            if member.status in ['creator', 'administrator']:
                return False

            try:
                await bot.delete_message(chat_id=telegram_chat_message.chat_id,
                                         message_id=telegram_chat_message.message_id, )
                await repo.deleted_telegram_chat_message(id=telegram_chat_message.id)
                await repo.add_telegram_chat_member_rating(
                    from_chat_member_id=None, in_chat_member_id=telegram_chat_member.id, value=-0.1,
                    status=TelegramChatMemberRatingStatus.ACTIVE
                )
            except:
                pass

    async def message_via_bot_trottled(self, message: Message, data: dict):
        telegram_chat: TelegramChat = data['telegram_chat']
        telegram_chat_message: TelegramChatMessage = data['telegram_chat_message']
        telegram_chat_member = data['telegram_chat_member']
        bot: Bot = data['bot']

        if not telegram_chat.members_can_send_message_via_bot and message.via_bot:
            member = await GetChatMember(chat_id=telegram_chat_message.chat_id, user_id=telegram_chat_message.user_id)
            if member.status in ['creator', 'administrator']:
                return False

            try:
                await bot.delete_message(chat_id=telegram_chat_message.chat_id,
                                         message_id=telegram_chat_message.message_id, )
                await repo.deleted_telegram_chat_message(id=telegram_chat_message.id)
                await repo.add_telegram_chat_member_rating(
                    from_chat_member_id=None, in_chat_member_id=telegram_chat_member.id, value=-0.5,
                    status=TelegramChatMemberRatingStatus.ACTIVE
                )
            except:
                pass

    async def forward_message_trottled(self, message: Message, data: dict):
        telegram_chat: TelegramChat = data['telegram_chat']
        telegram_chat_message = data['telegram_chat_message']
        telegram_chat_member = data['telegram_chat_member']
        bot: Bot = data['bot']

        if not telegram_chat.members_can_forward_message and (message.forward_from
                                                              or message.forward_from_chat):
            member = await GetChatMember(chat_id=telegram_chat_message.chat_id, user_id=telegram_chat_message.user_id)
            if member.status in ['creator', 'administrator']:
                return False

            try:
                await bot.delete_message(chat_id=telegram_chat_message.chat_id,
                                         message_id=telegram_chat_message.message_id, )
                await repo.deleted_telegram_chat_message(id=telegram_chat_message.id)
                await repo.add_telegram_chat_member_rating(
                    from_chat_member_id=None, in_chat_member_id=telegram_chat_member.id, value=-1,
                    status=TelegramChatMemberRatingStatus.ACTIVE
                )
            except:
                pass

    async def message_link_trottled(self, message: Message, data: dict):
        telegram_chat: TelegramChat = data['telegram_chat']
        telegram_chat_message = data['telegram_chat_message']
        telegram_chat_member = data['telegram_chat_member']
        bot: Bot = data['bot']

        text = message.text or message.caption
        if not text:
            return False
        loggers.middlewares.debug(re.findall(r'htts?://.+', text))
        loggers.middlewares.debug(re.findall(r'tg?m?e?:?/?/.+', text))
        if not telegram_chat.members_can_send_link and (
                re.findall(r'tg?\.?m?e?:?/?/.+', text) or re.findall(r'https?://.+', text)
        ):
            member = await GetChatMember(chat_id=telegram_chat_message.chat_id, user_id=telegram_chat_message.user_id)
            if member.status in ['creator', 'administrator']:
                return False

            try:
                await bot.delete_message(chat_id=telegram_chat_message.chat_id,
                                         message_id=telegram_chat_message.message_id, )
                await repo.deleted_telegram_chat_message(id=telegram_chat_message.id)
                await repo.add_telegram_chat_member_rating(
                    from_chat_member_id=None, in_chat_member_id=telegram_chat_member.id, value=-5,
                    status=TelegramChatMemberRatingStatus.ACTIVE
                )
            except:
                pass

    async def message_mention_bot_trottled(self, message: Message, data: dict):
        telegram_chat: TelegramChat = data['telegram_chat']
        telegram_chat_message = data['telegram_chat_message']
        telegram_chat_member = data['telegram_chat_member']
        bot: Bot = data['bot']

        text = message.text or message.caption
        if not text:
            return False

        if not telegram_chat.members_can_mention_bot and re.findall(r'@?[a-zA-Z][\w]{,28}[Bb][Oo][Tt]', text, re.ASCII):
            member = await GetChatMember(chat_id=telegram_chat_message.chat_id, user_id=telegram_chat_message.user_id)
            if member.status in ['creator', 'administrator']:
                return False

            try:
                await bot.delete_message(chat_id=telegram_chat_message.chat_id,
                                         message_id=telegram_chat_message.message_id, )
                await repo.deleted_telegram_chat_message(id=telegram_chat_message.id)
                await repo.add_telegram_chat_member_rating(
                    from_chat_member_id=None, in_chat_member_id=telegram_chat_member.id, value=-4,
                    status=TelegramChatMemberRatingStatus.ACTIVE
                )
            except:
                pass


class TelegramChatEditedMessageMiddleware(BaseMiddleware):

    async def __call__(self, handler, event: Message, data):
        repo: Repo = data['repo']
        telegram_chat_message = await repo.get_telegram_chat_message(
            message_id=event.message_id, chat_id=event.chat.id
        )
        if not telegram_chat_message:
            return await handler(event, data)

        if event.text and event.text != telegram_chat_message.message_text:
            await repo.edited_text_telegram_chat_message(id=telegram_chat_message.id, message_text=event.text)
        elif event.caption and event.caption != telegram_chat_message.message_text:
            await repo.edited_text_telegram_chat_message(id=telegram_chat_message.id, message_text=event.caption)
        else:
            return await handler(event, data)

        loggers.middlewares.debug(
            f'Сообщение изменено. '
            f'[message_id:{telegram_chat_message.message_id}] [chat_id:{telegram_chat_message.chat_id}]'
        )

        telegram_chat_message = await repo.get_telegram_chat_message(
            message_id=event.message_id, chat_id=event.chat.id
        )

        data['telegram_chat_message'] = telegram_chat_message

        return await handler(event, data)


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.message.outer_middleware(TelegramChatMessageMiddleware())
    dispatcher.edited_message.outer_middleware(TelegramChatEditedMessageMiddleware())
