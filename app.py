from flask import Flask
from dotenv import dotenv_values
from server.views import PageRoutes
from server.api import ApiRoutes
from database import DatabaseSettings
from database import create_database_handler
import os

# Constants
ENV_CONFIGS: dict = dotenv_values(".env")
TEMPLATES_DIR: str = "server/templates"
STATIC_DIR: str = "server/static"

# Create the Flask server.
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# Secret key
secret_key = os.environ.get('SECRET_KEY')
app.secret_key = secret_key

# Create the database handler.
database_settings = DatabaseSettings(
    name=ENV_CONFIGS['DATABASE_NAME'],
    host=ENV_CONFIGS['DATABASE_HOST'],
    port=ENV_CONFIGS['DATABASE_PORT'],
    username=ENV_CONFIGS['DATABASE_USERNAME'],
    password=ENV_CONFIGS['DATABASE_PASSWORD']
)
database_handler = create_database_handler(database_settings)
database_handler.connect()

# Register the routes for page views and REST API.
app.register_blueprint(PageRoutes)
app.register_blueprint(ApiRoutes)
