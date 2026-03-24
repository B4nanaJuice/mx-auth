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
    
# Getters
def get_user_by_id(id: int) -> User | None:
    user: User | None = db.session.execute(db.select(User).where(User.id == id)).scalar_one_or_none()
    return user

def get_user_by_public_id(public_id: str) -> User | None:
    user: User | None = db.session.execute(db.select(User).where(User.public_id == public_id)).scalar_one_or_none()
    return user

def get_user_by_email(email: str) -> User | None:
    user: User | None = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
    return user