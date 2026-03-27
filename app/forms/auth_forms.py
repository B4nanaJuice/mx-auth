# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Regexp, Length

# Register form
class RegisterForm(FlaskForm):
    # Public ID, username, email address, password
    public_id: StringField = StringField(
        label = 'Public ID', 
        validators = [
            DataRequired(message = 'Public ID is required'),
            Length(min = 3, max = 32, message = 'Public ID must contain between 3 and 32 chars'),
            Regexp(regex = r'^[a-z0-9_]+$', message = 'Public ID must contain only lowercase letters, digits and underscores')
        ])
    username: StringField = StringField(
        label = 'Username', 
        validators = [
            DataRequired(message = 'Username is required'),
            Length(min = 3, max = 32, message = 'Username must contain between 3 and 32 chars'),
            Regexp(regex = r'^[a-zA-Z0-9_]*$', message = 'Username must contain only letters, digits and underscores')
        ])
    email: EmailField = EmailField(
        label = 'Email Address', 
        validators = [
            DataRequired(message = 'Email address is required'),
            Length(max = 255, message = 'Email address must contain at most 255 chars')
        ])
    password: PasswordField = PasswordField(
        label = 'Password', 
        validators = [
            DataRequired(message = 'Password is required'),
            Length(min = 8, max = 64, message = 'Password must contain between 8 and 64 chars'),
            Regexp(regex = r'^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^a-zA-Z0-9])([^\s]){8,64}$', message = 'Password must contain at least one lowercase letter, one uppercase letter, one digit and one special char')
        ])
    
# Login form
class LoginForm(FlaskForm):
    # Identifier, password
    identifier: StringField = StringField(
        label = 'Email Address or public ID (@)',
        validators = [
            DataRequired(message = 'Email address or public ID is required')
        ])
    password: PasswordField = PasswordField(
        label = 'Password',
        validators = [
            DataRequired(message = 'Password is required')
        ])