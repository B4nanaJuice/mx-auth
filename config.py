# Imports
from os import getenv

# Create config static class
class Config:
    # Database information
    SQLALCHEMY_DATABASE_URI: str = getenv('SQLALCHEMY_DATABASE_URI', 'sqlite://')