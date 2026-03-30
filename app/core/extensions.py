# Imports
from flask import request, redirect, url_for, flash
from functools import wraps
import jwt

from config.settings import config
from app.models.user import User
from app.services.auth_service import AuthService

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_login_required(*args, **kwargs):
        # If logged : access token up to date
        # If not up to date : if refresh token active (check db) -> ok
        token: str = request.cookies.get('access_token', type = str, default = None)
        if not token:
            flash(message = 'You must be logged to access this.', category = 'error')
            return redirect(url_for('auth.login', next = request.url))
        
        try:
            access_token: dict = jwt.decode(token,
                                            key = config.JWT_SECRET_KEY,
                                            algorithms = [config.JWT_ALGORITHM])
            
            user_id: int = access_token['user_id']
            user: User = AuthService.get_user(user_id = user_id)
            return f(user, *args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return redirect(url_for('auth.refresh', next = request.url))

        except Exception as e:
            flash(message = 'Something went wrong with your token. Please login again.', category = 'error')
            return redirect(url_for('auth.login', next = request.url))
        
    return decorated_login_required

