from flask import Flask
from server.views import PageRoutes

# Constants
TEMPLATES_DIR: str = "server/templates"
STATIC_DIR: str = "server/static"

# Create the Flask server.
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# Register the routes for page views.
app.register_blueprint(PageRoutes)
