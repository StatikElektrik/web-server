from flask import Flask
from server.views import PageRoutes
from server.api import ApiRoutes

# Constants
TEMPLATES_DIR: str = "server/templates"
STATIC_DIR: str = "server/static"

# Create the Flask server.
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# Register the routes for page views and REST API.
app.register_blueprint(PageRoutes)
app.register_blueprint(ApiRoutes)
