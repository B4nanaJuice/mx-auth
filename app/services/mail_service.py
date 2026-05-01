# Imports
import logging

# Create logger
logger = logging.getLogger(__name__)

# Create custom exception class
class MailException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message: str = message
        self.status_code: int = status_code

# Create static class
class MailService:
    
    @staticmethod
    def send_mail(content: str) -> None:
        print(content)
        return