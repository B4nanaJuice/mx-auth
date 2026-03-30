# Imports
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.data.database import db
from app.models.token import Token

# Create user model
class User(db.Model):
    __tablename__ = 'users'

    # Attributes 
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    public_id: Mapped[str] = mapped_column(db.String(32), unique = True, nullable = False, index = True)
    username: Mapped[str] = mapped_column(db.String(32), nullable = False)
    email: Mapped[str] = mapped_column(db.String(255), unique = True, nullable = False, index = True)
    password: Mapped[str] = mapped_column(db.String(255), nullable = False)
    role: Mapped[str] = mapped_column(db.String(16), nullable = False, default = 'user')

    is_active: Mapped[bool] = mapped_column(nullable = False, default = True)
    is_verified: Mapped[bool] = mapped_column(nullable = False, default = False)

    # Login tracking
    login_attempts: Mapped[int] = mapped_column(nullable = False, default = 0)
    locked_until: Mapped[datetime] = mapped_column(nullable = True)
    last_login_at: Mapped[datetime] = mapped_column(nullable = True)
    last_login_ip: Mapped[str] = mapped_column(db.String(45), nullable = True)

    created_at: Mapped[datetime] = mapped_column(nullable = False, default = lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(nullable = False, default = lambda: datetime.now(timezone.utc), onupdate = datetime.now(timezone.utc))
 
    # Relationships
    tokens: Mapped[List['Token']] = relationship(cascade = 'all, delete-orphan')
 
    @property
    def is_locked(self) -> bool:
        if self.locked_until and datetime.fromisoformat(self.locked_until.isoformat() + '+00:00') > datetime.now(timezone.utc):
            return True
        return False
 
    def record_login(self, ip: str | None = None):
        self.login_attempts = 0
        self.locked_until = None
        self.last_login_at = datetime.now(timezone.utc)
        self.last_login_ip = ip
 
    def increment_failed_login(self, max_attempts: int = 5, lockout_minutes: int = 15):
        self.login_attempts += 1
        if self.login_attempts >= max_attempts:
            self.locked_until = datetime.now(timezone.utc) + timedelta(minutes = lockout_minutes)
            self.login_attempts = 0
 
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'created_at': self.created_at.isoformat(),
        }
 
    def __repr__(self) -> str:
        return f'<User {self.username!r} ({self.role})>'