# Imports
import logging

from app.data.models.oauth import OAuthClient
from app.data.models.authorization_code import AuthorizationCode
from app.data.database import db

# Create logger
logger = logging.getLogger(__name__)

# Create custom exception class
class OAuthException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message: str = message
        self.status_code: int = status_code

class OAuthService:

    @staticmethod
    def register_external_app(name: str, url: str) -> OAuthClient:
        
        app: OAuthClient = OAuthClient(
            name = name,
            url = url
        )

        db.session.add(app)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            existing: OAuthClient | None = OAuthClient.query.filter(OAuthClient.name == name).first()

            if not existing:
                logger.warning(f'Something went wrong while trying to register external application {app.name}')
                raise OAuthException(f'Something went wrong while registering the external application.')
            raise OAuthException(f'This external application already exists', 409)
            
        logger.info(f'New external application registered: {app.name} ({app.id})')
        return app

    @staticmethod
    def get_app_by_id(app_id: int) -> OAuthClient:
        app: OAuthClient = OAuthClient.query.filter(OAuthClient.id == app_id).first()
        if not app:
            raise OAuthException(f'App not found with the ID {app_id}')
        return app
    
    @staticmethod
    def get_app_by_name(name: str) -> OAuthClient:
        app: OAuthClient = OAuthClient.query.filter(OAuthClient.name == name).first()
        if not app:
            raise OAuthException(f'App not found with the name {name}')
        return app

    @staticmethod
    def generate_auth_code(oauth_client: int, user_id: int) -> AuthorizationCode:

        code: AuthorizationCode = AuthorizationCode(
            oauth_client = oauth_client,
            owner_id = user_id
        )

        db.session.add(code)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            logger.warning(f'Something went wrong while adding authorization code {code}')
            raise OAuthException(f'Something went wrong while generating your authorization code.')
        
        return code