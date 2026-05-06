# Imports
import logging

from app.data.models.app import ExternalApp
from app.data.database import db

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
    def register_external_app(name: str, url: str) -> ExternalApp:
        
        app: ExternalApp = ExternalApp(
            name = name,
            url = url
        )

        db.session.add(app)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            existing: ExternalApp | None = ExternalApp.query.filter(ExternalApp.name == name).first()

            if not existing:
                logger.warning(f'Something went wrong while trying to register external application {app.name}')
                raise AppException(f'Something went wrong while registering the external application.')
            raise AppException(f'This external application already exists', 409)
            
        logger.info(f'New external application registered: {app.name} ({app.id})')
        return app

    @staticmethod
    def get_app_by_id(app_id: int) -> ExternalApp:
        app: ExternalApp = ExternalApp.query.filter(ExternalApp.id == app_id).first()
        if not app:
            raise AppException(f'App not found with the ID {app_id}')
        return app
    
    @staticmethod
    def get_app_by_name(name: str) -> ExternalApp:
        app: ExternalApp = ExternalApp.query.filter(ExternalApp.name == name).first()
        if not app:
            raise AppException(f'App not found with the name {name}')
        return app