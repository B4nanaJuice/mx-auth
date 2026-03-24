# Imports
from flask import Flask
from dotenv import load_dotenv

from extensions.database import init_db
from extensions.jwt import init_secret

# Load environment variables
load_dotenv()

# Init flask app
app: Flask = Flask('mx-auth')
init_db(app = app)
init_secret(app = app)