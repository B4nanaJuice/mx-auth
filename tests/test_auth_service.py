# Imports
from flask import Flask
import pytest

from tests.test_user import create_user
from app.data.models.user import User
from app.services.auth_service import AuthService, AuthException
from app.services.token_service import TokenService

# Tests on user service
def test_register(app: Flask):
    with app.app_context():

        public_id: str = 'pytest'
        username: str = 'PyTest'
        email: str = 'pytest@example.com'
        password: str = 'passWORD1*'

        user: User = AuthService.register(
            public_id = public_id,
            username = username,
            email = email,
            password = password
        )

        assert user.public_id == public_id
        assert user.id is not None
        assert user.password != password

        with pytest.raises(AuthException):
            AuthService.register(
                public_id = public_id,
                username = 'user',
                email = 'email@email.email',
                password = 'password'
            )

            AuthService.register(
                public_id = 'public',
                username = 'username',
                email = email,
                password = 'pass'
            )

def test_verify_user(app: Flask):
    with app.app_context():

        user: User = AuthService.register('public_id', 'username', 'email', 'password')
        assert user.is_verified is False

        AuthService.verify_user(user.public_id)
        assert user.is_verified is True

        with pytest.raises(AuthException):
            AuthService.verify_user(user.public_id)
            AuthService.verify_user('no_existing')

def test_login(app: Flask):
    with app.app_context():

        user: User = AuthService.register('public_id', 'username', 'email', 'password')

        with pytest.raises(AuthException):
            AuthService.login('public_id', 'password')

        AuthService.verify_user(user.public_id)
        AuthService.login(user.public_id, 'password')

        with pytest.raises(AuthException) as e:
            AuthService.login('public_id', 'wrong_password_here')
            AuthService.login('wrong_id', 'password')
            AuthService.login('public_id', 'wrong_password_here')
            AuthService.login('public_id', 'wrong_password_here')
            AuthService.login('public_id', 'wrong_password_here')
            # Should be locked now
            AuthService.login('public_id', 'password')

def test_logout(app: Flask):
    with app.app_context():

        user: User = AuthService.register('public_id', 'username', 'email', 'password')
        AuthService.verify_user(user.public_id)
        token_pair = AuthService.login('public_id', 'password')
        assert token_pair is not None

        AuthService.logout(token_pair.refresh_token)
        assert TokenService.is_token_revoked(token_pair.refresh_token) is True

def test_change_password(app: Flask):
    with app.app_context():

        user: User = AuthService.register('public_id', 'username', 'email', 'password')
        AuthService.verify_user(user.public_id)
        token_pair = AuthService.login('public_id', 'password')
        assert TokenService.is_token_revoked(token_pair.refresh_token) is False

        AuthService.change_password(user.id, 'password', 'new_password')
        assert TokenService.is_token_revoked(token_pair.refresh_token) is True

        with pytest.raises(AuthException):
            AuthService.login('public_id', 'password')
            AuthService.change_password(-1, 'new_password', 'password')
            AuthService.change_password(user.id, 'password', 'other_password')
            AuthService.change_password(user.id, 'new_password', 'new_password')

        token_pair = AuthService.login(user.email, 'new_password')
        assert TokenService.is_token_revoked(token_pair.refresh_token) is False