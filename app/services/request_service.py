# Imports
import logging
import re
import jwt

from config.settings import config

# Create logger
logger = logging.getLogger(__name__)

# Create custom exception class
class RequestException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message: str = message
        self.status_code: int = status_code

# Create static class
class RequestService:
    
    # Check if redirect url is in allowed redirects
    @staticmethod
    def is_allowed_redirect(next_url: str) -> bool:
        return True