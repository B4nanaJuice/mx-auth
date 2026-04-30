# Imports
from flask import Flask
import pytest
import re
import jwt
from datetime import datetime, timedelta, timezone

from app.data.models.token import Token
from app.services.token_service import TokenService, TokenException, TokenPair
from config.settings import config
from app.data.database import db

# Tests on token service
def test_create_token_pair(app: Flask):
    with app.app_context():
        
        token_pair = TokenService.create_token_pair(1)
        assert token_pair is not None
        assert type(token_pair) == TokenPair
        assert token_pair.access_token is not None
        assert token_pair.refresh_token is not None

        assert re.match(r'^.*\..*\..*$', token_pair.access_token) is not None
        assert re.match(r'^.*\..*\..*$', token_pair.refresh_token) is not None

def test_verify_token_pair(app: Flask):
    with app.app_context():
        
        token_pair: TokenPair = TokenService.create_token_pair(user_id = 1)
        assert TokenService.verify_token_pair(token_pair.access_token, token_pair.refresh_token) is True
        assert TokenService.verify_token_pair('abc', token_pair.refresh_token) is False

        fake_token: str = jwt.encode({}, key = config.JWT_ACCESS_TOKEN_SECRET_KEY, algorithm = config.JWT_ALGORITHM)
        assert TokenService.verify_token_pair(fake_token, token_pair.refresh_token) is False

        fake_token: str = jwt.encode({'user_id': 4}, key = config.JWT_ACCESS_TOKEN_SECRET_KEY, algorithm = config.JWT_ALGORITHM)
        assert TokenService.verify_token_pair(fake_token, token_pair.refresh_token) is False

        fake_token = jwt.encode({}, key = config.JWT_REFRESH_TOKEN_SECRET_KEY, algorithm = config.JWT_ALGORITHM)
        assert TokenService.verify_token_pair(token_pair.access_token, fake_token) is False

        fake_token = jwt.encode({'value': 'a'}, key = config.JWT_REFRESH_TOKEN_SECRET_KEY, algorithm = config.JWT_ALGORITHM)
        assert TokenService.verify_token_pair(token_pair.access_token, fake_token) is False

def test_refresh_access_token(app: Flask):
    with app.app_context():
        
        token_pair: TokenPair = TokenService.create_token_pair(user_id = 1)
        new_pair = TokenService.refresh_access_token(token_pair.refresh_token)
        assert new_pair is not None
        assert type(new_pair) == TokenPair

        fake_token: str = jwt.encode({}, key = config.JWT_REFRESH_TOKEN_SECRET_KEY, algorithm = config.JWT_ALGORITHM)
        with pytest.raises(TokenException):
            TokenService.refresh_access_token(fake_token)

        fake_token = jwt.encode({'value': 'a'}, key = config.JWT_REFRESH_TOKEN_SECRET_KEY, algorithm = config.JWT_ALGORITHM)
        with pytest.raises(TokenException):
            TokenService.refresh_access_token(fake_token)

def test_revoke_token(app: Flask):
    with app.app_context():
        
        token_pair: TokenPair = TokenService.create_token_pair(user_id = 1)
        assert TokenService.is_token_revoked(token_pair.refresh_token) is False

        TokenService.revoke_token(token_pair.refresh_token)
        assert TokenService.is_token_revoked(token_pair.refresh_token) is True

def test_revoke_all_tokens(app: Flask):
    with app.app_context():
        
        TokenService.create_token_pair(user_id = 1)
        TokenService.create_token_pair(user_id = 1)
        assert TokenService.revoke_all_tokens(user_id = 1) == 2

        TokenService.create_token_pair(user_id = 1)
        assert TokenService.revoke_all_tokens(user_id = 1) == 1

        assert TokenService.revoke_all_tokens(user_id = 1) == 0

def test_is_token_revoked(app: Flask):
    with app.app_context():

        token_pair: TokenPair = TokenService.create_token_pair(user_id = 1)
        assert TokenService.is_token_revoked(token_pair.refresh_token) is False

        with pytest.raises(jwt.exceptions.InvalidSignatureError):
            TokenService.is_token_revoked(token_pair.access_token)
            TokenService.is_token_revoked('key')

        fake_token = jwt.encode({'value': 'a'}, key = config.JWT_REFRESH_TOKEN_SECRET_KEY, algorithm = config.JWT_ALGORITHM)
        assert TokenService.is_token_revoked(fake_token) is True

def test_purge_expired_tokens(app: Flask):
    with app.app_context():
        
        token_pair: TokenPair = TokenService.create_token_pair(user_id = 1)
        assert TokenService.purge_expired_tokens() == 0

        refresh_token_value = jwt.decode(token_pair.refresh_token, config.JWT_REFRESH_TOKEN_SECRET_KEY, [config.JWT_ALGORITHM]).get('value')
        token: Token = Token.query.filter(Token.value == refresh_token_value).first()
        token.expires_at = datetime.now(timezone.utc) - timedelta(minutes = 1)
        db.session.commit()
        assert TokenService.purge_expired_tokens() == 1