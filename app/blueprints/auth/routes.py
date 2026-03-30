# Imports
from flask import Blueprint, request, flash, redirect, url_for, render_template, Response, make_response, jsonify

from app.forms.auth_forms import RegisterForm, LoginForm, PasswordChangeForm
from app.services.auth_service import AuthService, AuthError
from app.services.request_service import RequestService
from app.services.token_service import TokenService
from app.core.extensions import login_required

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

            next_redirect: str = request.args.get('next', type = str, default = None)

            flash(message = 'Successfully logged in !', category = 'success')
            response: Response = make_response(redirect(RequestService.verify_url(next_redirect) if next_redirect else url_for('auth.me')))
            response.set_cookie('access_token', token_pair.get('access_token'))
            response.set_cookie('refresh_token', token_pair.get('refresh_token'))
            return response
        
        except AuthError as e:
            flash(message = e.message, category = 'error')

    return render_template('auth/login.html', form = login_form)

# Refresh token
@bp.get('/refresh')
def refresh():

    access_token: str = request.cookies.get('access_token', type = str, default = None)
    refresh_token: str = request.cookies.get('refresh_token', type = str, default = None)
    next_redirect: str = request.args.get('next', type = str, default = None)

    user_id, user_role = TokenService.verify_token_pair(access_token = access_token, refresh_token = refresh_token)

    if user_id == -1:
        flash(message = 'Something went wrong with your session token. Please login again.', category = 'warning')
        return redirect(url_for('auth.login'))
    
    access_token = TokenService.refresh_access_token(user_id = user_id, user_role = user_role)

    response: Response = make_response(redirect(RequestService.verify_url(next_redirect) if next_redirect else url_for('auth.me')))
    response.set_cookie('access_token', access_token)
    return response
    

# Profile page
@bp.get('/me')
@login_required
def me(current_user):
    password_change_form: PasswordChangeForm = PasswordChangeForm()
    return render_template('auth/profile.html', user = current_user, form = password_change_form)

# Change password route
@bp.post('/me/password')
@login_required
def change_password(current_user):
    
    password_change_form: PasswordChangeForm = PasswordChangeForm()
    if password_change_form.validate_on_submit():
        try:
            AuthService.change_password(
                user_id = current_user.id,
                current_password = password_change_form.current_password.data,
                new_password = password_change_form.new_password.data
            )

            flash(message = 'Your password has been changed ! All sessions have been invalidated.', category = 'success')
        
        except AuthError as e:
            flash(message = e.message, category = 'error')

    return redirect(url_for('auth.me'))