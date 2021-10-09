import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class TelegramChatMessage(BaseModel):
    """Таблица сообщений телеграм чатов."""
    __tablename__ = 'telegram_chat_messages'
    id = sa.Column(sa.BigInteger(), sa.Sequence('telegram_chat_messages_id_seq'), primary_key=True, autoincrement=True)
    message_id = sa.Column(sa.BigInteger(), nullable=True)
    message_text = sa.Column(sa.String(4096))
    is_deleted = sa.Column(sa.Boolean(), default=False)

    chat_id = sa.Column(sa.ForeignKey('telegram_chats.id', ondelete='CASCADE'), nullable=False)
    user_id = sa.Column(sa.ForeignKey('telegram_users.id', ondelete='CASCADE'), nullable=False)
    date = sa.Column(sa.DateTime(), server_default=sa.func.now())

    user: 'TelegramUser' = relationship('TelegramUser', uselist=False)
    chat: 'TelegramChat' = relationship('TelegramChat', uselist=False)
