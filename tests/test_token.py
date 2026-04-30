# Imports
from flask import Flask
from datetime import datetime, timedelta, timezone
import jwt
import os

from app.data.database import db
from app.data.models.token import Token
from app.data.models.user import User
from tests.test_user import create_user
from config.settings import config

# Method to create a token
def create_token() -> Token:

    user: User = create_user()

    token: Token = Token(
        value = jwt.encode({'value': os.urandom(32).hex()}, key = config.JWT_REFRESH_TOKEN_SECRET_KEY, algorithm = config.JWT_ALGORITHM),
        owner_id = user.id
    )

    db.session.add(token)
    db.session.commit()

    return token

def test_token_validity(app: Flask):
    with app.app_context():
        
        token: Token = create_token()
        assert token.is_valid is True
        assert token.created_at.replace(tzinfo = timezone.utc) <= datetime.now(timezone.utc)

        token.expires_at = datetime.now(timezone.utc) - timedelta(minutes = 1)
        assert token.is_valid is False

        token.expires_at = datetime.now(timezone.utc) - timedelta(days = 50)
        assert token.is_valid is False

        token.expires_at = datetime.now(timezone.utc) + timedelta(minutes = 1)
        assert token.is_valid is True

        token.expires_at = datetime.now(timezone.utc) + timedelta(days = 120)
        assert token.is_valid is True

def test_token_to_dict(app: Flask):
    with app.app_context():
        
        token: Token = create_token()
        
        keys = set(token.to_dict().keys())
        expected = {'id', 'value', 'owner_id', 'created_at', 'expires_at'}
        assert expected.issubset(keys)

        token_dict: dict = token.to_dict()
        assert token_dict['id'] == token.id
        assert token_dict['value'] == token.value
        assert token_dict['owner_id'] == token.owner_id
        assert 'random_key' not in token_dict

def test_token_repr(app: Flask):
    with app.app_context():
        
        token: Token = create_token()
        assert str(token).startswith('<Token ')
        assert token.value[:10] in str(token)
        assert token.value not in str(token)