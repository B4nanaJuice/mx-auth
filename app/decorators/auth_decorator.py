# Imports
from functools import wraps
from flask import request, redirect, url_for
import jwt
from typing import Dict

from config.settings import config
from app.services import UserService
from app.data.models.user import User

def access_token_required(f):
    @wraps(f)
    def _f(*args, **kwargs):
        
        access_token: str = request.cookies.get('access_token', None)
        if access_token:
            try:
                access_data: Dict[str, any] = jwt.decode(
                    jwt = access_token,
                    key = config.JWT_ACCESS_TOKEN_SECRET_KEY,
                    algorithms = [config.JWT_ALGORITHM]
                )

                user: User = UserService.get_user_by_id(id = access_data.get('user_id'))
                return f(user, *args, **kwargs)
            except:
                pass

        return redirect(url_for('auth.refresh_token', next = request.url))

    return _f

def refresh_token_required(f):
    @wraps(f)
    def _f(*args, **kwargs):

        refresh_token: str = request.cookies.get('refresh_token', None)
        print(refresh_token)
        if refresh_token:
            return f(refresh_token, *args, **kwargs)
        return redirect(url_for('auth.login', next = request.url))
    
    return _f