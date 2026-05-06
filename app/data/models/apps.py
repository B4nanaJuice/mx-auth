# Imports
from sqlalchemy.orm import Mapped, mapped_column
import os

from app.data.database import db

# Create token class
class ExternalApp(db.Model):
    __tablename__ = 'apps'

    # Attributes
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(nullable = False, unique = True)
    url: Mapped[str] = mapped_column(nullable = False)
    access_token_secret: Mapped[str] = mapped_column(nullable = False, default = lambda: os.urandom(32).hex())
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url
        }
    
    def __repr__(self) -> str:
        return f'<ExternalApp {self.name}>'