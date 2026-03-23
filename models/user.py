# Imports
from sqlalchemy.orm import Mapped, mapped_column

from extensions.database import db

# Create class model
class User(db.Model):
    __tablename__ = 'users'

    # Attributes
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(nullable = False)
    email: Mapped[str] = mapped_column(nullable = False, unique = True)
    password: Mapped[str] = mapped_column(nullable = False)

    def __repr__(self) -> str:
        return f'<User {self.name}>'