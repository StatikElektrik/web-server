from flask import Flask
from flask import render_template

# Constants
TEMPLATES_DIR: str = "server/templates"
STATIC_DIR: str = "server/static"

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

@app.route('/')
def index():
    return render_template('index.html')
