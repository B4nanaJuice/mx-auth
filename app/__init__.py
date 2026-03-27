# Imports
from flask import Flask, jsonify

from config import config
from app.core.extensions import init_db
from app.blueprints import auth_blueprint

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(config)
    init_db(app = app)

    @app.get('/health')
    def get_health():
        return jsonify({'status': 'ok'}), 200

    app.register_blueprint(auth_blueprint)
    
    return app