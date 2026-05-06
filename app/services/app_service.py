# Imports
import logging

from app.data.models.apps import ExternalApp

# Create logger
logger = logging.getLogger(__name__)

# Create custom exception class
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message: str = message
        self.status_code: int = status_code

class AppService:

    @staticmethod
    def get_app_by_id(app_id: int) -> ExternalApp:
        app: ExternalApp = ExternalApp.query.find(ExternalApp.id == app_id).first()
        if not app:
            raise AppException(f'App not found with the ID {app_id}')
        return app
    
    @staticmethod
    def get_app_by_name(name: str) -> ExternalApp:
        app: ExternalApp = ExternalApp.query.find(ExternalApp.name == name).first()
        if not app:
            raise AppException(f'App not found with the name {name}')
        return app