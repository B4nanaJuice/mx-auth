# Imports
from flask import Blueprint, request, flash, redirect, url_for, render_template, Response, make_response, jsonify

from app.forms import RegisterForm, LoginForm
from app.services import AuthService, AuthError

# Create blueprint
bp: Blueprint = Blueprint(name = 'auth', import_name = __name__, url_prefix = '/auth')

# Register route
@bp.route('/register', methods = ['GET', 'POST'])
def register():
    
    register_form: RegisterForm = RegisterForm()
    if register_form.validate_on_submit():
        try:
            AuthService.register(
                public_id = register_form.public_id.data,
                username = register_form.username.data,
                email = register_form.email.data,
                password = register_form.password.data
            )

            flash(message = 'Account created successfully ! You may now login', category = 'success')
            return redirect(url_for('auth.login'))
        
        except AuthError as e:
            flash(message = e.message, category = 'error')
            
    return render_template('auth/register.html', form = register_form)
    
# Login route
@bp.route('/login', methods = ['GET', 'POST'])
def login():

    login_form: LoginForm = LoginForm()
    if login_form.validate_on_submit():
        try:
            token_pair: dict = AuthService.login(
                identifier = login_form.identifier.data,
                password = login_form.password.data,
                ip = request.remote_addr
            )

            flash(message = 'Successfully logged in !', category = 'success')
            response: Response = make_response(redirect(url_for('auth.me')))
            response.set_cookie('access_token', token_pair.get('access_token'))
            response.set_cookie('refresh_token', token_pair.get('refresh_token'))
            return response
        
        except AuthError as e:
            flash(message = e.message, category = 'error')

    return render_template('auth/login.html', form = login_form)

# Profile page
@bp.get('/me')
def me():
    return jsonify({
        'access_token': request.cookies.get('access_token'),
        'refresh_token': request.cookies.get('refresh_token')
    }), 200