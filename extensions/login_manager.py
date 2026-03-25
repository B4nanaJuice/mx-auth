# Imports
from flask import request, redirect, url_for, flash, Response
from functools import wraps
import jwt
from datetime import datetime, timezone, timedelta

from config import Config
from models.user import User, get_user_by_public_id

# Create login required decorator
def login_required(f):
    
    @wraps(f)
    def decorated(*args, **kwargs):
        jwt_token: str = request.cookies.get('jwt_token', type = str, default = None)

        if not jwt_token:
            flash(message = 'You need to be logged to access this.', category = 'error')
            return redirect(url_for('auth.login', next = request.url))
        
        try:
            data: dict = jwt.decode(jwt_token, Config.SECRET_KEY, algorithms = ['HS256'])
            current_user: User | None = get_user_by_public_id(data.get('public_id'))

            if not current_user:
                flash(message = 'The account associated with your token does not exist. Please log in again.', category = 'error')
                return redirect(url_for('auth.login', next = request.url))
        except jwt.ExpiredSignatureError:
            flash(message = 'Your token has expired. Please log in again.', category = 'error')
            return redirect(url_for('auth.login', next = request.url))
        except:
            flash(message = 'A problem occured. Please log in again.', category = 'error')
            return redirect(url_for('auth.login', next = request.url))
        
        return f(current_user, *args, **kwargs)
    return decorated

# Create token refresher method
def refresh_token(response: Response):
    # Get the token
    jwt_token: str = request.cookies.get('jwt_token', type = str, default = None)
    if not jwt_token:
        return response

    # Check the expiration
    try:
        data: dict = jwt.decode(jwt_token, Config.SECRET_KEY, algorithms = ['HS256'])
        expiration = data.get('exp')
        if not expiration:
            return response
        
        data['exp'] = datetime.now(timezone.utc) + timedelta(hours = 1)
        response.set_cookie('jwt_token', jwt_token)
        return response
    
    except jwt.ExpiredSignatureError:
        flash(message = 'Your token has expired. If you want to access your personnal space, please log in again.', category = 'warning')
        return response
    except:
        flash(message = 'A problem occured with your session token. Please log in again.', category = 'warning')
        return response