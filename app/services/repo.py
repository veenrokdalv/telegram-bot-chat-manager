import datetime as dt
from typing import Optional, Union

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.models.telegram_chat import TelegramChat
from app.models.telegram_chat_member import TelegramChatMember
from app.models.telegram_chat_message import TelegramChatMessage
from app.models.telegram_user import TelegramUser


class NotFoundTarget(Exception):
    """Класс ошибки, когда запись не найдена во время изменения данных."""


class Repo:

    def __init__(self, db_session: sessionmaker, db_engine: AsyncEngine):
        self.db_session = db_session
        self.db_engine = db_engine

    async def get_telegram_user(self, id: int) -> Optional[TelegramUser]:
        """Возвращает телеграм пользователя с базы данных."""

        stmt = sa.select(TelegramUser).filter_by(id=id)

        async with self.db_session() as session:
            return (await session.execute(stmt)).scalar()

    async def add_telegram_user(self, **kwargs: int) -> TelegramUser:
        """Добавляет и возвращает телеграм пользователя с базы данных."""

        async with self.db_session.begin() as session:
            _user = TelegramUser(
                id=int(kwargs.pop('id')), join_date=kwargs.pop('join_date', dt.datetime.utcnow())
            )
            async with self.db_session.begin():
                session.add(_user)
            return _user

    async def get_telegram_chat(self, id: int) -> Optional[TelegramChat]:
        """Возвращает телеграм чат с базы данных."""

        stmt = sa.select(TelegramChat).filter_by(id=id)

        async with self.db_session() as session:
            return (await session.execute(stmt)).scalar()

    async def add_telegram_chat(self, **kwargs: int) -> TelegramChat:
        """Добавляет и возвращает телеграм чат с базы данных."""

        async with self.db_session.begin() as session:
            _chat = TelegramChat(
                id=int(kwargs.pop('id')), join_date=kwargs.pop('join_date', dt.datetime.utcnow())
            )
            async with self.db_session.begin():
                session.add(_chat)
            return _chat

    async def get_telegram_chat_member(self, user_id: int, chat_id: int) -> Optional[TelegramChatMember]:
        """Возвращает участника телеграм чат с базы данных."""

        stmt = sa.select(TelegramChatMember).filter_by(user_id=user_id, chat_id=chat_id)

        async with self.db_session() as session:
            return (await session.execute(stmt)).scalar()

    async def add_telegram_chat_member(self, **kwargs: int) -> TelegramChatMember:
        """Добавляет и возвращает участника телеграм чат с базы данных."""

        async with self.db_session.begin() as session:
            _chat_member = TelegramChatMember(
                chat_id=int(kwargs.pop('chat_id')), user_id=int(kwargs.pop('user_id')),
                join_date=kwargs.pop('join_date', dt.datetime.utcnow())
            )
            async with self.db_session.begin():
                session.add(_chat_member)
            return _chat_member

    async def get_telegram_chat_message(self, message_id: int, chat_id: int) -> Optional[TelegramChatMessage]:
        """Возвращает сообщение из телеграм чата с базы данных."""
        stmt = sa.select(TelegramChatMessage).filter_by(message_id=message_id, chat_id=chat_id)

        async with self.db_session() as session:
            return (await session.execute(stmt)).scalar()

    async def get_telegram_chat_messages_from_chat_member(
            self, user_id: int, chat_id: int, datetime_interval: dt.timedelta, as_int: bool = False
    ) -> Union[int, list[TelegramChatMessage]]:
        """Возвращает список или число сообщений участника телеграм чата с базы данных."""
        stmt_as_list = sa.select(TelegramChatMessage).filter_by(user_id=user_id, chat_id=chat_id).filter(
            TelegramChatMessage.date >= dt.datetime.utcnow() - datetime_interval
        )
        stmt_as_int = sa.select(sa.func.count(TelegramChatMessage.id)).filter_by(user_id=user_id, chat_id=chat_id).filter(
            TelegramChatMessage.date >= dt.datetime.utcnow() - datetime_interval
        )

        async with self.db_session() as session:
            if as_int:
                return (await session.execute(stmt_as_int)).scalar()

            return (await session.execute(stmt_as_list)).scalars().all()

    async def add_telegram_chat_message(self, **kwargs):
        """Создает и возвращает сообщение из телеграм чата с базы данных."""
        _chat_message = TelegramChatMessage(
            message_id=kwargs.pop('message_id'),
            message_text=kwargs.pop('message_text'),
            is_deleted=kwargs.pop('is_deleted', False),
            chat_id=kwargs.pop('chat_id'),
            user_id=kwargs.pop('user_id'),
            date=kwargs.pop('date', dt.datetime.utcnow()),
        )
        async with self.db_session.begin() as session:
            session.add(_chat_message)
        return _chat_message

    async def edited_text_telegram_chat_message(self, id: int, message_text: str) -> None:
        """Обновляет поле message_text сообщения из телеграм чата в базе данных."""
        stmt = sa.update(TelegramChatMessage).values(message_text=message_text).filter_by(id=id)
        async with self.db_session.begin() as session:
            await session.execute(stmt)

    async def deleted_telegram_chat_message(self, id: int) -> None:
        """Обновляет поле is_delete сообщения из телеграм чата в базе данных."""
        stmt = sa.update(TelegramChatMessage).values(is_deleted=True).filter_by(id=id)
        async with self.db_session.begin() as session:
            await session.execute(stmt)