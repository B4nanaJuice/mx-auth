# Imports
from flask import Flask
import pytest

from tests.test_user import create_user
from app.data.models.user import User
from app.services.user_service import UserService, UserException

# Tests on user service
def test_get_user_by_public_id(app: Flask):
    with app.app_context():

        _user: User = create_user()

        public_id: str = _user.public_id
        user = UserService.get_user_by_public_id(public_id = public_id)
        assert user is not None
        assert user.username == _user.username
        assert _user.email == user.email
        assert user.public_id == public_id

        with pytest.raises(UserException):
            UserService.get_user_by_public_id(public_id = 'public_id')
            UserService.get_user_by_public_id(public_id = 57)
            UserService.get_user_by_public_id(public_id = _user)
            

def test_get_user_by_id(app: Flask):
    with app.app_context():

        _user: User = create_user()

        id: int = _user.id
        user = UserService.get_user_by_id(id = id)
        assert user is not None
        assert user.username == _user.username
        assert _user.email == user.email
        assert user.id == id

        with pytest.raises(UserException):
            UserService.get_user_by_id(id = 'public_id')
            UserService.get_user_by_id(id = 92)
            UserService.get_user_by_id(id = _user)

def test_get_user_by_email(app: Flask):
    with app.app_context():

        _user: User = create_user()

        email: str = _user.email
        user = UserService.get_user_by_email(email = email)
        assert user is not None
        assert user.username == _user.username
        assert _user.email == user.email
        assert user.email == email

        with pytest.raises(UserException):
            UserService.get_user_by_email(email = 'email')
            UserService.get_user_by_email(email = -1)
            UserService.get_user_by_email(email = _user)

def test_get_user_by_identifier(app: Flask):
    with app.app_context():

        _user: User = create_user()

        email: str = _user.email
        public_id: str = _user.public_id

        user_by_email = UserService.get_user_by_identifier(identifier = email)
        user_by_public_id = UserService.get_user_by_identifier(identifier = public_id)

        assert user_by_email is not None
        assert user_by_public_id is not None
        assert user_by_public_id.username == user_by_email.username

        with pytest.raises(UserException):
            UserService.get_user_by_identifier(identifier = 'identifier')
            UserService.get_user_by_identifier(identifier = 0.86)
            UserService.get_user_by_identifier(identifier = _user)