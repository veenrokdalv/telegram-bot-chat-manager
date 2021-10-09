import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class TelegramChatMember(BaseModel):
    """Таблица участников телеграм чата."""
    __tablename__ = 'telegram_chat_members'
    id = sa.Column(sa.BigInteger(), sa.Sequence('telegram_chat_members_id_seq'), primary_key=True, autoincrement=True)
    chat_id = sa.Column(sa.ForeignKey('telegram_chats.id', ondelete='CASCADE'), nullable=False)
    user_id = sa.Column(sa.ForeignKey('telegram_users.id', ondelete='CASCADE'), nullable=False)
    join_date = sa.Column(sa.DateTime(), server_default=sa.func.now())

    user: 'TelegramUser' = relationship('TelegramUser', uselist=False)
    chat: 'TelegramChat' = relationship('TelegramChat', uselist=False)
