# Imports
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Regexp, Length

class RegisterForm(FlaskForm):
    public_id: StringField = StringField(
        label = 'Public ID',
        validators = [DataRequired(), Regexp(r'^[a-z0-9_]+$'), Length(min = 3, max = 32)],
        description = 'Enter the name that will be used as your unique ID.',
        _prefix = '@'
    )

    username: StringField = StringField(
        label = 'Username',
        validators = [DataRequired(), Regexp(r'^.+$'), Length(min = 3, max = 64)],
        description = 'Enter the name that will be displayed on your account.'
    )

    email: EmailField = EmailField(
        label = 'Email',
        validators = [DataRequired()],
        description = 'Enter your email address.'
    )

    password: PasswordField = PasswordField(
        label = 'Password',
        validators = [DataRequired(), Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')],
        description = 'Enter your password here. It must contain at least 8 characters, one lowercase letter, one uppercase letter, one digit and one special character.'
    )

    # recaptcha: RecaptchaField = RecaptchaField()

class LoginForm(FlaskForm):
    identifier: StringField = StringField(
        label = 'Public ID or Email',
        validators = [DataRequired()],
        description = 'Enter your public ID (begins with @) or your email address.'
    )

    password: PasswordField = PasswordField(
        label = 'Password',
        validators = [DataRequired()],
        description = 'Enter your password.'
    )

class ChangePasswordForm(FlaskForm):
    pass

class RequestPasswordResetForm(FlaskForm):
    identifier: StringField = StringField(
        label = 'Public ID or Email',
        validators = [DataRequired()],
        description = 'Enter your public ID (begins with @) or your email address.'
    )

class ResetPasswordForm(FlaskForm):
    password: PasswordField = PasswordField(
        label = 'New password',
        validators = [DataRequired(), Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')],
        description = 'Enter your new password here. It must contain at least 8 characters, one lowercase letter, one uppercase letter, one digit and one special character.'
    )