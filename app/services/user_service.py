# Imports
import logging

from app.data.models.user import User

# Create logger
logger = logging.getLogger(__name__)

# Create custom exception class
class UserException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message: str = message
        self.status_code: int = status_code

# Create static class
class UserService:
    
    # Get user from its public_id
    @staticmethod
    def get_user_by_public_id(public_id: str) -> User:
        user: User | None = User.query.filter(User.public_id == public_id).first()
        if not user:
            raise UserException(f'User not find with the public ID {public_id}')
        return user
    
    # Get user from its id
    @staticmethod
    def get_user_by_id(id: int) -> User:
        user: User | None = User.query.filter(User.id == id).first()
        if not user:
            raise UserException(f'User not found with the ID {id}')
        return user
    
    # Get user from its email
    @staticmethod
    def get_user_by_email(email: str) -> User:
        user: User | None = User.query.filter(User.email == email).first()
        if not user:
            raise UserException(f'User not found with email {email}')
        return user
    
    # Get user by identifier
    @staticmethod
    def get_user_by_identifier(identifier: str) -> User:
        user: User = User.query.filter((User.public_id == identifier)|(User.email == identifier)).first()
        if not user:
            raise UserException(f'User not found with email or public_id {identifier}')
        return user