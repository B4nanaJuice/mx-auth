# Imports
import jwt
from datetime import datetime, timezone, timedelta
import os
import logging

from app.core import db
from app.models import Token
from config import config

logger = logging.getLogger(__name__)

# Create static class
class TokenService:
    
    # Create token pair
    @staticmethod
    def create_token_pair(user_id: int, additional_claims: dict | None = None) -> dict:
        claims: dict = additional_claims or {}
        
        access_token: str = jwt.encode({'user_id': user_id, 'exp': datetime.now(timezone.utc) + timedelta(hours = 1)} | claims,
                                       key = config.JWT_SECRET_KEY,
                                       algorithm = config.JWT_ALGORITHM)

        token: str = os.urandom(32).hex()
        db.session.add(Token(
            value = token,
            owner_id = user_id
        ))
        db.session.commit()

        refresh_token: str = jwt.encode({'token': token} | claims,
                                        key = config.JWT_SECRET_KEY,
                                        algorithm = config.JWT_ALGORITHM)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    # Refresh access token
    @staticmethod
    def refresh_access_token(user_id: int, user_role: str) -> dict:

        access_token: str = jwt.encode({'user_id': user_id, 'exp': datetime.now(timezone.utc) + timedelta(hours = 1), 'role': user_role},
                                       key = config.JWT_SECRET_KEY,
                                       algorithm = config.JWT_ALGORITHM)
        
        return {
            'access_token': access_token
        }
    
    # Revoke token
    @staticmethod
    def revoke_token(encoded_token: str) -> None:
        data: dict = jwt.decode(encoded_token,
                                config.JWT_SECRET_KEY,
                                algorithms = [config.JWT_ALGORITHM])
        
        Token.query.filter(Token.value == data['token']).delete()
        db.session.commit()

        return
    
    # Revoke all user tokens
    @staticmethod
    def revoke_all_user_tokens(user_id: int) -> None:
        Token.query.filter(Token.owner_id == user_id).delete()
        db.session.commit()

        logger.info(f'All tokens revoked for user_id {user_id}')

        return
    
    # Is Token revoked
    @staticmethod
    def is_token_revoked(token: str) -> bool:
        return Token.query.filter(Token.value == token).first() == None
    
    # Purge all expired tokens
    @staticmethod
    def purge_expired_tokens() -> int:
        now = datetime.now(timezone.utc)
        deleted = Token.query.filter(Token.expires_at < now).delete()
        db.session.commit()

        logger.info(f'Purged {deleted} expired tokens.')
        return deleted