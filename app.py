# Imports
from flask import Flask, Response
from dotenv import load_dotenv

from extensions.database import init_db
from extensions.jwt import init_secret
from extensions.login_manager import refresh_token

from routes import auth, account

# Load environment variables
load_dotenv()

# Init flask app
app: Flask = Flask('mx-auth')
init_db(app = app)
init_secret(app = app)

# Register all blueprints
app.register_blueprint(blueprint = auth.page)
app.register_blueprint(blueprint = account.page)

# Add home route
@app.route('/')
def home():
    return 'Hello world !'

# Add after request token refresher
@app.after_request
def refresh_jwt_token(response: Response):
    return refresh_token(response = response)