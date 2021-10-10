import sqlalchemy as sa

from app.models.base import BaseModel


class TelegramChat(BaseModel):
    """Таблица чатов телеграм."""
    __tablename__ = 'telegram_chats'
    id = sa.Column(sa.BigInteger(), nullable=False, primary_key=True, unique=True)
    use_flood_control = sa.Column(sa.Boolean(), default=True)
    members_can_forawrd_message = sa.Column(sa.Boolean(), default=True)
    members_can_send_message_via_bot = sa.Column(sa.Boolean(), default=True)
    members_can_send_video = sa.Column(sa.Boolean(), default=True)
    members_can_send_photo = sa.Column(sa.Boolean(), default=True)
    members_can_send_document = sa.Column(sa.Boolean(), default=True)
    members_can_mention_bot = sa.Column(sa.Boolean(), default=True)
    members_can_send_link = sa.Column(sa.Boolean(), default=True)
    join_date = sa.Column(sa.DateTime(), server_default=sa.func.now())