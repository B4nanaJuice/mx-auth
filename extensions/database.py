# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from config import Config

# Create Base
class Base(DeclarativeBase):
    pass

# Init db
db: SQLAlchemy = SQLAlchemy(model_class = Base)

# Method for db connection
def init_db(app: Flask) -> None:
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app = app)

    with app.app_context():
        db.create_all()