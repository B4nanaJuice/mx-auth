# Imports
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Base config class
class BaseConfig:
    # Core
    SECRET_KEY: str = os.getenv('SECRET_KEY', '635f6b642c93ebdbad005b34b4899bdde3f05a0a9491d5497087bd1b28444c7d329bda1e643f0d52713c4098a240627a')
    DEBUG: bool = False
    TESTING: bool = False

    # Database
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URL', 'sqlite:///mx-auth.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    # JWT
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', '80bd0e8c37699dbb7a486dbb00562d463b9659d9fd60a8f420ec74903329fa29')
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(seconds = int(os.getenv('JWT_TOKEN_ACCESS_EXPIRES', 15*60)))
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(seconds = os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 30*24*60*60))
    JWT_TOKEN_LOCATION: list = ["headers", "cookies"]
    JWT_COOKIE_SECURE: bool = False
    JWT_COOKIE_CSRF_PROTECT: bool = True
    JWT_BLACKLIST_ENABLED: bool = True
    JWT_BLACKLIST_TOKEN_CHECKS: list = ["access", "refresh"]

    # Security
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds = 5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds = 10)

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True

_config_map = {
    "development": DevelopmentConfig,
    "test": TestConfig,
    "production": ProductionConfig
}

def get_config() -> BaseConfig:
    env = os.getenv('FLASK_ENV', 'development').lower()
    return _config_map.get(env, DevelopmentConfig)

config = get_config()