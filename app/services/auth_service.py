# Imports
import logging
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.data.database import db
from app.services.token_service import TokenService

logger = logging.getLogger(__name__)

class AuthError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

# Create static class
class AuthService:

    # Registration
    @staticmethod
    def register(public_id: str, username: str, email: str, password: str) -> User:
        password_hash: str = generate_password_hash(password = password)
        user: User = User(
            public_id = public_id.strip().lower(),
            username = username.strip(),
            email = email.strip().lower(),
            password = password_hash
        )

        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError: 
            db.session.rollback()
            existing: User | None = User.query.filter((User.public_id == public_id.strip().lower()) | (User.email == email.strip().lower())).first()

            if existing and existing.public_id == public_id:
                raise AuthError(message = 'Public ID is already taken.', status_code = 409)
            raise AuthError(message = 'Email is already taken.', status_code = 409)
        
        logger.info(f'New user registered: {user.username} ({user.id})')
        return user

    # Login
    @staticmethod
    def login(identifier: str, password: str, ip: str | None = None) -> dict:
        identifier = identifier.strip().lower()
        user: User = User.query.filter((User.public_id == identifier) | (User.email == identifier)).first()
        if not user:
            raise AuthError(message = 'Invalid credentials.', status_code = 401)
        
        if not user.is_active:
            raise AuthError(message = 'This account has been deactivated.', status_code = 403)

        if user.is_locked:
            raise AuthError(message = 'Account temporarily locked due to too many failed attempts. Try again later.', status_code = 403)
        
        if not check_password_hash(user.password, password):
            user.increment_failed_login()
            db.session.commit()
            raise AuthError(message = 'Invalid credentials.', status_code = 401)
        
        user.record_login(ip = ip)
        db.session.commit()

        token_pair: dict = TokenService.create_token_pair(user_id = user.id, additional_claims = {'role': user.role})
        logger.info(f'User logged in: {user.username} ({user.id}) from {ip}')
        return token_pair

    # Logout
    @staticmethod
    def logout(refresh_token: str) -> None:
        TokenService.revoke_token(encoded_token = refresh_token)
        logger.info(f'User logged out')

        return 

    # Refresh token
    def refresh(user_id: int, user_role: str) -> dict:
        return TokenService.refresh_access_token(user_id = user_id, user_role = user_role)

    # Change password
    @staticmethod
    def change_password(user_id: int, current_password: str, new_password: str) -> None:
        user: User = User.query.get(user_id)
        if not User:
            raise AuthError(message = 'User not found.', status_code = 404)
        
        if not check_password_hash(user.password, current_password):
            raise AuthError(message = 'Current password is incorrect.', status_code = 401)
        
        user.password = generate_password_hash(new_password)
        db.session.commit()

        TokenService.revoke_all_user_tokens(user_id = user_id)
        logger.info(f'Password changed for user_id = {user_id}')

        return

    # Get user
    @staticmethod
    def get_user(user_id: int) -> User:
        user: User = User.query.get(user_id)
        if not user:
            raise AuthError(message = 'User not found.', status_code = 404)
        return user