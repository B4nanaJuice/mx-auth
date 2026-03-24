# Imports
from flask import Flask

from config import Config

# Method for secret key setup
def init_secret(app: Flask) -> None:
    app.config['SECRET_KEY'] = Config.SECRET_KEY