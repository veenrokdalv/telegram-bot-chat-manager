from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher.filters import BaseFilter
from aiogram.methods import GetChatMember
from aiogram.types import Message

import loggers


class HasPermissionFilter(BaseFilter):
    """Фильтр доступа участника телеграм чата"""
    member_permissions: Union[list[str], str]

    async def __call__(self, message: Message, telegram_chat_member, **kwargs):
        member = await GetChatMember(chat_id=telegram_chat_member.chat_id, user_id=telegram_chat_member.user_id)
        if member.status == 'creator':
            loggers.filters.debug('User is creator, has permission - true')
            return {'chat_member': member}
        elif member.status == 'member':
            loggers.filters.debug('User is member, has permission - false')
            return False
        elif member.status == 'left':
            loggers.filters.debug('User is left, has permission - false')
            return False
        elif member.status == 'banned':
            loggers.filters.debug('User is banned, has permission - false')
            return False

        if isinstance(self.member_permissions, str):
            self.member_permissions = [self.member_permissions]

        for alowed_member_permission in self.member_permissions:
            for member_permission, value in member.dict().items():
                if alowed_member_permission == member_permission and value:
                    return True


def setup(dispatcher: Dispatcher, *args, **kwargs):
    dispatcher.message.bind_filter(HasPermissionFilter)



class MyFilter(BoundFilter):
    key = 'only_admins'

    def __init__(self, only_admins):
        self.only_admins = only_admins
        self.admins_ids = conf.admins_ids


    async def check(self, event, **kwargs):
        if self.only_admins:
            return event.from_user.id in self.only_admins