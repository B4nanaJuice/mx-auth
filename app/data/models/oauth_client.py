# Imports
import os
from sqlalchemy.orm import mapped_column, Mapped

from app.data.database import db

class OAuthClient(db.Model):
    __tablename__ = 'oauth_clients'

    # Attributes
    id: Mapped[str] = mapped_column(db.String(16), primary_key = True)
    name: Mapped[str] = mapped_column(db.String(32), nullable = False, unique = True)
    redirect_uri: Mapped[str] = mapped_column(db.String(64), nullable = False, unique = True)
    secret: Mapped[str] = mapped_column(db.String(96), nullable = False, unique = True, default = lambda: os.urandom(48).hex())

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'redirect_uri': self.redirect_uri
        }
    
    def __repr__(self) -> str:
        return f'<OAuthClient {self.id}>'