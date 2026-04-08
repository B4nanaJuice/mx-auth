# Imports
from flask import Flask
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone

from app.data.database import db
from app.data.models.user import User

# Method to quickly create a user
def create_user() -> User:

    user: User = User(
        public_id = 'pytest_user',
        username = 'PyTest',
        email = 'pytest@example.com',
        password = generate_password_hash('pytestPassword1*')
    )

    db.session.add(user)
    db.session.commit()

    return user
    
# Tests on user
def test_user_locked(app: Flask):
    with app.app_context():

        user: User = create_user()

        assert user.is_locked is False
        
        user.locked_until = datetime.now(timezone.utc)
        user.locked_until += timedelta(minutes = 10)
        assert user.is_locked is True

        user.locked_until -= timedelta(minutes = 20)
        assert user.is_locked is False

        user.locked_until += timedelta(days = 30)
        assert user.is_locked is True

        user.locked_until -= timedelta(days = 60)
        assert user.is_locked is False

def test_user_record_login(app: Flask):
    with app.app_context():

        user: User = create_user()

        assert user.login_attempts == 0

        user.record_login()
        assert user.login_attempts == 0
        assert user.locked_until is None

        user.login_attempts = 4
        user.record_login(ip = '127.0.0.1')
        assert user.login_attempts == 0
        assert user.last_login_ip == '127.0.0.1'

        user.record_login(ip = '2001:db8::1')
        assert user.last_login_ip == '2001:db8::1'

        before: datetime = datetime.now(timezone.utc) - timedelta(seconds = 10)
        after: datetime = datetime.now(timezone.utc) + timedelta(seconds = 10)
        user.record_login()
        assert before <= user.last_login_at.replace(tzinfo = timezone.utc) <= after

def test_user_incremental_login(app: Flask):
    with app.app_context():

        user: User = create_user()
        assert user.login_attempts == 0

        user.increment_failed_login()
        assert user.login_attempts == 1

        user.login_attempts = 0
        for i in range(3):
            user.increment_failed_login()
        assert user.login_attempts == 3

        user.login_attempts = 4
        user.increment_failed_login()
        assert user.locked_until is not None
        assert user.login_attempts == 5
        assert user.locked_until > datetime.now(timezone.utc)

        user.record_login()
        assert user.locked_until is None
        assert user.login_attempts == 0

def test_user_to_dict(app: Flask):
    with app.app_context():

        user: User = create_user()

        keys = set(user.to_dict().keys())
        expected = {'id', 'public_id', 'username', 'email', 'role', 'is_active', 'is_verified', 'last_login_at', 'created_at'}
        assert expected.issubset(keys)

        user_dict: dict = user.to_dict()
        assert user_dict['id'] is not None
        assert user_dict['public_id'] == 'pytest_user'
        assert user_dict['username'] == 'PyTest'
        assert user_dict['email'] == 'pytest@example.com'
        assert user_dict['is_active'] is True
        assert user_dict['role'] == 'user'
        assert 'password' not in user_dict
        
def test_user_repr(app: Flask):
    with app.app_context():

        user: User = create_user()
        assert 'PyTest' in str(user)
        assert str(user).startswith('<User ')
        assert 'user' in str(user)
        assert user.password not in str(user)