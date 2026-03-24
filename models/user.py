# Imports
from sqlalchemy.orm import Mapped, mapped_column

from extensions.database import db

# Create class model
class User(db.Model):
    __tablename__ = 'users'

    # Attributes
    id: Mapped[int] = mapped_column(db.Integer, primary_key = True, autoincrement = True)
    public_id: Mapped[str] = mapped_column(db.String(50), unique = True)
    name: Mapped[str] = mapped_column(db.String(100), nullable = False)
    email: Mapped[str] = mapped_column(db.String(70), nullable = False, unique = True)
    password: Mapped[str] = mapped_column(db.String(80), nullable = False)

    def __repr__(self) -> str:
        return f'<User {self.name}>'
