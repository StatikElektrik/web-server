from flask import Blueprint
from flask import render_template

# This route is for serving the HTML files.
PageRoutes = Blueprint('PageRoutes', __name__)

@PageRoutes.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@PageRoutes.route('/about-us', methods=['GET'])
def about_us():
    return render_template('about_us.html')

@PageRoutes.route('/project-details', methods=['GET'])
def project_details():
    return render_template('project_details.html')