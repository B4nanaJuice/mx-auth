# Imports
from flask import Flask
from dotenv import load_dotenv

from extensions.database import init_db

# Load environment variables
load_dotenv()

# Init flask app
app: Flask = Flask(__name__)
init_db(app = app)