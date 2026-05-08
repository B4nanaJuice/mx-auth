# Imports
import os
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from app.data.database import db
from config.settings import config

class AuthorizationCode(db.Model):
    __tablename__ = 'authorization_codes'

    # Attributes
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    code: Mapped[str] = mapped_column(db.String(8), nullable = False, unique = True, default = lambda: os.urandom(4).hex())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    oauth_client_id: Mapped[str] = mapped_column(ForeignKey('oauth_clients.id'))
    created_at: Mapped[datetime] = mapped_column(nullable = False, default = lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(nullable = False, default = lambda: datetime.now(timezone.utc) + config.AUTHORIZATION_CODE_EXPIRES)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'code': self.code,
            'owner_id': self.user_id,
            'oauth_client_id': self.oauth_client_id,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
        }
    
    def __repr__(self) -> str:
        return f'<AuthorizationCode {self.code}>'