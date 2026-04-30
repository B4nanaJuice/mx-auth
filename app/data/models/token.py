# Imports
from datetime import datetime, timezone
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.data.database import db
from config.settings import config

# Create token class
class Token(db.Model):
    __tablename__ = 'tokens'

    # Attributes
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    value: Mapped[str] = mapped_column(db.String(64), unique = True, index = True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(nullable = False, default = lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(nullable = False, default = lambda: datetime.now(timezone.utc) + config.JWT_REFRESH_TOKEN_EXPIRES)

    @property
    def is_valid(self) -> bool:
        return datetime.now(timezone.utc) < self.expires_at.replace(tzinfo = timezone.utc)
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'value': self.value,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
        }
    
    def __repr__(self) -> str:
        return f'<Token {self.value[:10]}...>'