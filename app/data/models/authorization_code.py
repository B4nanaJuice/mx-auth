# Import
import os
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone, timedelta

from app.data.database import db
from config.settings import config

class AuthorizationCode(db.Model):
    __tablename__ = 'authorization_codes'

    # Attributes
    id: Mapped[int] = mapped_column(primary_key = True, nullable = False, autoincrement = True)
    code: Mapped[str] = mapped_column(unique = True, nullable = False, default = lambda: os.urandom(4).hex())
    oauth_client: Mapped[int] = mapped_column(ForeignKey('oauth_clients.id'))
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(nullable = False, default = lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(nullable = False, default = lambda: datetime.now(timezone.utc) + config.AUTHORIZATION_CODE_EXPIRES)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'code': self.code,
            'oauth_client': self.oauth_client,
            'owner_id': self.owner_id
        }

    def __repr__(self) -> str:
        return f'<AuthorizationCode {self.code}>'