# Imports
from flask import Flask, Blueprint, render_template, flash, request, redirect, url_for

from app.forms.auth import RegisterForm, LoginForm
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