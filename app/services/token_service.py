# Imports
import jwt
import logging
from datetime import datetime, timezone, timedelta
import os

from app.data.database import db
from app.data.models.token import Token
from config.settings import config

# Create logger
logger = logging.getLogger(__name__)

# Create custom exception class
class TokenException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message: str = message
        self.status_code: int = status_code

# Create custom class for token pair
class TokenPair:
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

# Create static class
class TokenService:
    
    # Create token pair
    @staticmethod
    def create_token_pair(user_id: int) -> TokenPair:
        
        access_token: str = jwt.encode(
            { 'user_id': user_id, 'exp': datetime.now(timezone.utc) + config.JWT_ACCESS_TOKEN_EXPIRES },
            key = config.JWT_ACCESS_TOKEN_SECRET_KEY,
            algorithm = config.JWT_ALGORITHM
        )

        refresh_token_value: str = os.urandom(config.JWT_REFRESH_TOKEN_SIZE).hex()
        token: Token = Token(
            value = refresh_token_value,
            owner_id = user_id
        )

        db.session.add(token)
        db.session.commit()

        refresh_token: str = jwt.encode(
            { 'value': refresh_token_value },
            key = config.JWT_REFRESH_TOKEN_SECRET_KEY,
            algorithm = config.JWT_ALGORITHM
        )

        return TokenPair(
            access_token = access_token,
            refresh_token = refresh_token
        )

    # Verify token_pair
    @staticmethod
    def verify_token_pair(access_token: str, refresh_token: str) -> bool:
        
        try:
            access_token_data: dict = jwt.decode(
                jwt = access_token,
                key = config.JWT_ACCESS_TOKEN_SECRET_KEY,
                algorithms = [config.JWT_ALGORITHM]
            )

            user_id: int = access_token_data.get('user_id')
        except:
            return False
        
        if not user_id:
            return False
        
        refresh_token_data: dict = jwt.decode(
            jwt = refresh_token,
            key = config.JWT_REFRESH_TOKEN_SECRET_KEY,
            algorithms = [config.JWT_ALGORITHM]
        )

        if 'value' not in refresh_token_data:
            return False

        token: Token = Token.query.filter(Token.value == refresh_token_data.get('value')).first()
        if not token:
            return False
        
        return token.owner_id == user_id

    # Refresh access token
    @staticmethod
    def refresh_access_token(refresh_token: str) -> TokenPair:
        
        refresh_token_data: dict = jwt.decode(
            jwt = refresh_token,
            key = config.JWT_REFRESH_TOKEN_SECRET_KEY,
            algorithms = [config.JWT_ALGORITHM]
        )

        if not 'value' in refresh_token_data:
            raise TokenException(f'Invalid refresh token.')
        
        token: Token = Token.query.filter(Token.value == refresh_token_data.get('value')).first()
        if not token:
            raise TokenException(f'No user corresponds to this token.')
        
        user_id: int = token.owner_id
        access_token: str = jwt.encode(
            { 'user_id': user_id, 'exp': datetime.now(timezone.utc) + config.JWT_ACCESS_TOKEN_EXPIRES },
            key = config.JWT_ACCESS_TOKEN_SECRET_KEY,
            algorithm = config.JWT_ALGORITHM
        )

        return TokenPair(
            access_token = access_token,
            refresh_token = refresh_token
        )

    # Revoke token
    @staticmethod
    def revoke_token(refresh_token: str) -> None:
        
        refresh_token_data: dict = jwt.decode(
            jwt = refresh_token,
            key = config.JWT_REFRESH_TOKEN_SECRET_KEY,
            algorithms = [config.JWT_ALGORITHM]
        )

        Token.query.filter(Token.value == refresh_token_data.get('value')).delete()
        db.session.commit()

        return

    # Revoke all user tokens
    @staticmethod
    def revoke_all_tokens(user_id: int) -> int:
        
        count: int = Token.query.filter(Token.owner_id == user_id).delete()
        db.session.commit()

        logger.info(f'{count} token{"s" if count != 1 else ""} revoked for user {user_id}')

        return count

    # Check if token is revoked
    @staticmethod
    def is_token_revoked(refresh_token: str) -> bool:
        
        refresh_token_data: dict = jwt.decode(
            jwt = refresh_token,
            key = config.JWT_REFRESH_TOKEN_SECRET_KEY,
            algorithms = [config.JWT_ALGORITHM]
        )

        token: Token = Token.query.filter(Token.value == refresh_token_data.get('value')).first()

        return token is None

    # Purge expired tokens
    @staticmethod
    def purge_expired_tokens() -> int:
        
        now: datetime = datetime.now(timezone.utc)

        count: int = Token.query.filter(Token.expires_at < now).delete()
        db.session.commit()

        logger.info(f'Purged {count} expired token{"s" if count != 1 else ""}')