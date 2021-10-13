import sqlalchemy as sa
from app.models.base import BaseModel


class TelegramChatMemberRating(BaseModel):
    __tablename__ = 'telegram_chat_member_ratings'

    id = sa.Column(sa.BigInteger(), sa.Sequence('telegram_chat_member_ratings_id_seq'), primary_key=True)
    from_chat_member = sa.Column(sa.ForeignKey('telegram_chat_members.id'))
    in_chat_member = sa.Column(sa.ForeignKey('telegram_chat_members.id'))
    value = sa.Column(sa.Float(2, True, 2), nullable=False)
    status = sa.Column(sa.String(32))