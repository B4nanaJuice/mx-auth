# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Database
class Base(DeclarativeBase):
    pass

db: SQLAlchemy = SQLAlchemy(model_class = Base)

def init_db(app: Flask) -> None:
    db.init_app(app = app)

    with app.app_context():
        db.create_all()

# Decorators
