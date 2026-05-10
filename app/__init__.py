# Imports
from flask import Flask, jsonify

from config.settings import config
from app.data.database import init_db
from app.cli import register_commands

from app.routes.auth import bp as auth_bp
from app.routes.oauth import bp as oauth_bp

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(config)
    init_db(app = app)
    register_commands(app = app)

    @app.get('/health')
    def get_health():
        return jsonify({'status': 'ok'}), 200
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(oauth_bp)
    
    return app