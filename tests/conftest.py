# Imports
import pytest

from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    yield app

@pytest.fixture
def client(app):
    return app.test_client()