# Imports
from werkzeug.security import generate_password_hash, check_password_hash
import pytest

from app.data.database import db
from app.data.models.user import User

def test_create_user(app):
    password: str = 'psw'
    user: User = User(public_id = 'pytest_user', 
                      username = 'PyTest', 
                      email = 'pytest@example.com', 
                      password = generate_password_hash(password))
    with app.app_context():    
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.public_id == 'pytest_user'
        assert user.username == 'PyTest'
        assert user.email == 'pytest@example.com'
        assert check_password_hash(user.password, password)