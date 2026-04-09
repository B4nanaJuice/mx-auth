# Imports
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Base config class
class BaseConfig:
    # Core
    SECRET_KEY: str = os.getenv('APP_SECRET_KEY', os.urandom(48).hex())
    DEBUG: bool = False
    TESTING: bool = False

    # Database
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URI', 'sqlite:///:memory:')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    # JWT
    JWT_ACCESS_TOKEN_SECRET_KEY: str = os.getenv('ACCESS_TOKEN_SECRET', os.urandom(48).hex())
    JWT_REFRESH_TOKEN_SECRET_KEY: str = os.getenv('REFRESH_TOKEN_SECRET', os.urandom(48).hex())
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(seconds = int(os.getenv('ACCESS_TOKEN_EXPIRES', 15 * 60)))
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(seconds = int(os.getenv('REFRESH_TOKEN_EXPIRES', 30 * 24 * 60 * 60)))
    JWT_REFRESH_TOKEN_SIZE: int = 48

    # Security
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15
    ALLOWED_REDIRECT_DOMAINS: list[str] = []

# Development config from base config class
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True

# Test config from base config class
class TestConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds = 30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes = 2)

# Production config from base config class
class ProductionConfig(BaseConfig):
    pass

_config_map = {
    "development": DevelopmentConfig,
    "test": TestConfig,
    "production": ProductionConfig
}

def get_config() -> BaseConfig:
    env = os.getenv('FLASK_ENV', 'development').lower()
    return _config_map.get(env, DevelopmentConfig)

config = get_config()