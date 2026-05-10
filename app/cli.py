# Imports
import click
from flask import current_app, Flask
from flask.cli import with_appcontext

from app.data.database import db
from app.data.models.user import User
from app.services.auth_service import AuthService
from app.services.token_service import TokenService
from app.services.oauth_service import OAuthService

# Method to register custom commands
def register_commands(app: Flask):
    app.cli.add_command(seed_db)
    app.cli.add_command(purge_tokens)
    return

# Method to create inital population
@click.command('seed-db')
@with_appcontext
def seed_db():

    OAuthService.create_oauth_client(
        id = 'test',
        name = 'Test',
        redirect_uri = 'localhost:1234'
    )
    
    try:
        admin: User = AuthService.register(
            public_id = 'admin',
            username = 'Admin',
            email = 'admin@example.com',
            password = 'password'
        )
        click.echo(f'Admin user has been created (id: {admin.id})')
    except:
        click.echo('Admin user already exists.')
    
    try:
        user: User = AuthService.register(
            public_id = 'user',
            username = 'User',
            email = 'user@example.com',
            password = 'password'
        )
        click.echo(f'User has been created (id: {user.id})')
    except:
        click.echo('User already exists.')

    return

# Method to purge tokens
@click.command('purge-tokens')
@with_appcontext
def purge_tokens():

    count: int = TokenService.purge_expired_tokens()
    click.echo(f'Purged {count} expired token{"s" if count != 1 else ""}.')