# Imports
import logging

from app.data.database import db
from app.data.models.oauth_client import OAuthClient
from app.data.models.authorization_code import AuthorizationCode
from app.services.token_service import TokenService, TokenPair

# Create logger
logger = logging.getLogger(__name__)

# Create custom exception class
class OAuthException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message: str = message
        self.status_code: int = status_code

# Create static class
class OAuthService:

    # Create a oauth client
    @staticmethod
    def create_oauth_client(id: str, name: str, redirect_uri: str) -> OAuthClient:

        client: OAuthClient = OAuthClient(
            id = id,
            name = name,
            redirect_uri = redirect_uri
        )

        db.session.add(client)
        db.session.commit()

        return client
    
    # Get OAuth client by its id
    @staticmethod
    def get_oauth_client_by_id(client_id: str) -> OAuthClient:
        client: OAuthClient = OAuthClient.query.filter(OAuthClient.id == client_id).first()
        if not client:
            raise OAuthException(f'Oauth client not found with id {client_id}', 404)
        return client
    
    # Get AUthorisation code by code
    @staticmethod
    def get_authorization_code_by_code(code: str) -> AuthorizationCode:
        auth_code: AuthorizationCode = AuthorizationCode.query.filter(AuthorizationCode.code == code).first()
        if not auth_code:
            raise OAuthException(f'Authorization code not found with code {code}', 404)
        return auth_code
    
    # Generate auth code
    @staticmethod
    def generate_authorization_code(user_id: int, oauth_client_id: str) -> AuthorizationCode:
        
        auth_code: AuthorizationCode = AuthorizationCode(
            user_id = user_id,
            oauth_client_id = oauth_client_id
        )

        db.session.add(auth_code)
        db.session.commit()

        return auth_code
    
    # Delete authorization code
    @staticmethod
    def delete_authorization_code(code: str) -> None:
        AuthorizationCode.query.filter(AuthorizationCode.code == code).delete()
        db.session.commit()
        return
    
    # Exchange auth code for token
    @staticmethod
    def exchange_authorization_code(code: str) -> TokenPair:

        # Get auth code object
        auth_code: AuthorizationCode = OAuthService.get_authorization_code_by_code(code = code)

        # Get oauth client
        oauth_client: OAuthClient = OAuthService.get_oauth_client_by_id(client_id = auth_code.oauth_client_id)

        # Get keys from authCode.oauth_client_id and authCode.user_id
        token_pair: TokenPair = TokenService.create_token_pair(
            user_id = auth_code.user_id,
            access_secret = oauth_client.access_secret,
            refresh_secret = oauth_client.refresh_secret,
            oauth_client_id = oauth_client.id
        )

        # Delete auth code
        OAuthService.delete_authorization_code(code = code)

        # Return token pair
        return token_pair