# Imports
from os import getenv

# Create config static class
class Config:
    # Database information
    SQLALCHEMY_DATABASE_URI: str = getenv('SQLALCHEMY_DATABASE_URI', 'sqlite://')

    # APP secret key
    SECRET_KEY: str = getenv('APP_SECRET')