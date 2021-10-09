import sqlalchemy as sa

from app.models.base import BaseModel


class TelegramUser(BaseModel):
    """Таблица пользователей телеграм."""
    __tablename__ = 'telegram_users'
    id = sa.Column(sa.BigInteger(), nullable=False, primary_key=True, unique=True)
    join_date = sa.Column(sa.DateTime(), server_default=sa.func.now())
