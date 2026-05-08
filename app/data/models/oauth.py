# Imports
import os
from sqlalchemy.orm import Mapped, mapped_column

from app.data.database import db

# Create token class
class OAuthClient(db.Model):
    __tablename__ = 'oauth_clients'

    # Attributes
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(db.String(64), nullable = False, unique = True)
    secret: Mapped[str] = mapped_column(db.String(64), nullable = False, default = lambda: os.urandom(32).hex())
    url: Mapped[str] = mapped_column(db.String(64), nullable = False)

    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url
        }
    
    def __repr__(self) -> str:
        return f'<OAuthClient {self.name}>'