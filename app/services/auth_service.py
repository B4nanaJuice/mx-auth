# Imports
import logging
from werkzeug.security import generate_password_hash, check_password_hash

from app.data.database import db
from app.services.token_service import TokenService
from app.services.user_service import UserService, UserException
from app.data.models.user import User

# Create logger
logger = logging.getLogger(__name__)

# Create custom exception class
class AuthException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message: str = message
        self.status_code: int = status_code

# Create static class
class AuthService:
    
    # Register new user
    @staticmethod
    def register(public_id: str, username: str, email: str, password: str) -> User:
        password_hash: str = generate_password_hash(password = password)
        user: User = User(
            public_id = public_id.lower().strip(),
            username = username.strip(),
            email = email.lower().strip(),
            password = password_hash
        )

        db.session.add(user)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            existing: User | None = User.query.filter((User.public_id == public_id.lower().strip())|(User.email == email.lower().strip())).first()

            if not existing:
                logger.warning(f'Something went wrong while trying to register user @{user.public_id}')
                raise AuthException(f'Something went wrong while registering.')
            
            if existing.public_id == user.public_id:
                raise AuthException(f'This public ID is already taken.', 409)
            
            if existing.email == user.email:
                raise AuthException(f'This email is already taken.', 409)
            
        logger.info(f'New user registered: @{user.public_id} ({user.id})')
        return user
    
    # Verify user account
    @staticmethod
    def verify_user(public_id: str) -> None:
        user: User = UserService.get_user_by_public_id(public_id = public_id)
        
        user.is_verified = True
        db.session.commit()

        return
    
    # Login the user
    @staticmethod
    def login(identifier: str, password: str, ip: str | None = None) -> dict[str, str]:
        identifier: str = identifier.strip().lower()

        try:
            user: User = UserService.get_user_by_identifier(identifier = identifier)
        except UserException:
            raise AuthException('Invalid creadentials.', 401)
        
        if not user.is_active:
            raise AuthException('This account is not activated yet. Please activate it before login again.', 403)
        
        if not user.is_locked:
            raise AuthException('This account is locked temporarily due to too many failed attempts. Please try again later.', 403)
        
        if not check_password_hash(pwhash = user.password, password = password):
            user.increment_failed_login()
            db.session.commit()
            raise AuthException('Invalid credentials.', 401)
        
        user.record_login(ip = ip)
        db.session.commit()

        token_pair: dict[str, str] = TokenService.create_token_pair(user_id = user.id)
        logger.info(f'User logged in: @{user.public_id} (ip = {ip})')
        return token_pair
    
    # Logout
    @staticmethod
    def logout(refresh_token: str) -> None:
        
        TokenService.revoke_token(refresh_token = refresh_token)
        return

    # Change password
    @staticmethod
    def change_password(user_id: int, current_password: str, new_password: str) -> None:
        
        try:
            user: User = UserService.get_user_by_id(id = user_id)
        except UserException:
            raise AuthException('Invalid credentials.')
        
        if not user or not check_password_hash(user.password, current_password):
            raise AuthException('Invalid credentials.')
        
        user.password = generate_password_hash(new_password)
        db.session.commit()

        TokenService.revoke_all_tokens(user_id = user_id)
        return