# Imports
from flask import Flask, Blueprint, render_template, flash, request, redirect, url_for

from app.forms.auth import RegisterForm, LoginForm, ChangePasswordForm, ResetPasswordForm, RequestPasswordResetForm
from app.services import AuthService, AuthException, UserException

# Create blueprint
bp: Blueprint = Blueprint('auth', 'auth', url_prefix = '/auth')

@bp.route('/register', methods = ['GET', 'POST'])
def register():
    
    register_form: RegisterForm = RegisterForm()
    if register_form.validate_on_submit():
        
        try:
            user = AuthService.register(
                public_id = register_form.public_id.data,
                username = register_form.username.data,
                email = register_form.email.data,
                password = register_form.password.data
            )

            print(url_for('auth.verify', token = user.verify_token))

            return render_template('auth/register_success.html')
        
        except AuthException as e:
            flash(e.message, 'error')
            return render_template('auth/register.html', form = register_form)
    
    return render_template('auth/register.html', form = register_form)

@bp.get('/verify')
def verify():
    verify_token: str = request.args.get('token', None)
    try:
        AuthService.verify_user(
            verify_token = verify_token
        )

    except AuthException as ae:
        flash(ae.message, 'error')
        return redirect(url_for('auth.login'))
    
    except UserException as ue:
        flash(ue.message, 'error')
        return redirect(url_for('auth.login'))
    
    flash('Your accont has been verified ! You can now login.', 'success')
    return redirect(url_for('auth.login'))
    

@bp.route('/login', methods = ['GET', 'POST'])
def login():

    login_form: LoginForm = LoginForm()
    if login_form.validate_on_submit():

        try:
            token_pair = AuthService.login(
                identifier = login_form.identifier.data,
                password = login_form.password.data
            )

            return f'access: {token_pair.access_token}, refresh: {token_pair.refresh_token}'
        
        except AuthException as e:
            flash(e.message, 'error')
            return render_template('auth/login.html', form = login_form)
        
    return render_template('auth/login.html', form = login_form)

@bp.route('/request-password-reset', methods = ['GET', 'POST'])
def request_password_reset():

    request_password_reset_form: RequestPasswordResetForm = RequestPasswordResetForm()
    if request_password_reset_form.validate_on_submit():

        try:
            token: str = AuthService.request_password_reset(
                identifier = request_password_reset_form.identifier.data
            )

            if not token:
                return redirect(url_for('auth.login'))

            print(url_for('auth.reset_password', token = token))
            return f'A link has been sent to your email if it is in the database.'
        
        except AuthException as e:
            flash(e.message, 'error')
            return redirect(url_for('auth.login'))
        
    return render_template('auth/request_password_reset.html', form = request_password_reset_form)
        

@bp.route('/reset-password', methods = ['GET', 'POST'])
def reset_password():

    reset_password_token: str = request.args.get('token', None)
    reset_password_form: ResetPasswordForm = ResetPasswordForm()
    if reset_password_form.validate_on_submit():

        try:
            AuthService.reset_password(
                reset_password_token = reset_password_token,
                new_password = reset_password_form.password.data
            )

            return f'Password changed, you can now login with the new password'
        
        except AuthException as e:
            flash(e.message, 'error')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form = reset_password_form)