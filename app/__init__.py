# Imports
from flask import Flask, jsonify

from config.settings import config
from app.data.database import init_db
from app.cli import register_commands

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(config)
    init_db(app = app)
    register_commands(app = app)

    @app.get('/health')
    def get_health():
        return jsonify({'status': 'ok'}), 200
    
    return app