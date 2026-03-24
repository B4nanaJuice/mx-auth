# Imports
from flask import Blueprint, request, redirect, url_for, render_template, Response, make_response, flash
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timezone, timedelta

from models.user import User, get_user_by_public_id, get_user_by_email
from extensions.database import db
from config import Config

# Create Blueprint
page: Blueprint = Blueprint(name = 'auth', 
                            import_name = __name__, 
                            template_folder = 'templates',
                            url_prefix = '/auth',
                            static_folder = 'static')

@page.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        public_id: str = request.form.get('public_id', type = str, default = None)
        name: str = request.form.get('name', type = str, default = None)
        email: str = request.form.get('email', type = str, default = None)
        password: str = request.form.get('password', type = str, default = None)

        # Check form data
        if None in [public_id, name, email, password]:
            flash(message = 'Please fill in all the required fields.', category = 'error')
            return redirect(url_for('auth.register'))
        
        # Check if fields are already taken
        if get_user_by_public_id(public_id = public_id):
            flash(message = 'An account already exists with this public ID.', category = 'warning')
            return redirect(url_for('auth.register'))
        
        if get_user_by_email(email = email):
            flash(message = 'An account already exists with this email.', category = 'warning')
            return redirect(url_for('auth.register'))
        
        # Hash password
        password = generate_password_hash(password)

        # Create user
        user: User = User(public_id = public_id,
                          name = name,
                          email = email,
                          password = password)
        
        # Add user to the database
        try:
            db.session.add(user)
            db.session.commit()
        except:
            print('En error occured while trying to add the user to the database.')

        # Redirect on login page
        flash(message = 'You successfully registerd ! You may now login.', category = 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@page.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        identifier: str = request.form.get('identifier', type = str, default = None)
        password: str = request.form.get('password', type = str, default = None)

        next_redirect = request.args.get('next', type = str, default = None)

        # Check form data
        if None in [identifier, password]:
            flash(message = 'Please fill in all the required fields.', category = 'error')
            return redirect(url_for('auth.login'))
        
        # Check credentials
        user: User | None = get_user_by_email(email = identifier) or get_user_by_public_id(public_id = identifier)
        if not user or not check_password_hash(user.password, password):
            flash(message = 'Invalid credentials.', category = 'error')
            return redirect(url_for('auth.login'))
        
        # Create JWT
        jwt_token: str = jwt.encode({'public_id': user.public_id, 'exp': datetime.now(timezone.utc) + timedelta(hours = 1)},
                                    key = Config.SECRET_KEY,
                                    algorithm = 'HS256')

        # Create response
        flash(message = f'Welcome back {user.name} !', category = 'success')
        response: Response = make_response(redirect(next_redirect if next_redirect else url_for('account.me')))
        response.set_cookie('jwt_token', jwt_token)
        return response

    return render_template('auth/login.html')