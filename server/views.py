from flask import Blueprint
from flask import render_template


from database import ProjectManagersHandler,VehiclesHandler

# This route is for serving the HTML files.
PageRoutes = Blueprint('PageRoutes', __name__)

@PageRoutes.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@PageRoutes.route('/about-us', methods=['GET'])
def about_us():
    # Retrieve the project managers from the database.
    project_managers = ProjectManagersHandler().get_all_information()
    return render_template('about_us.html', members=project_managers)

@PageRoutes.route('/project_details', methods=['GET'])
def project_details():
    return render_template('project_details.html')

@PageRoutes.route('/dashboard', methods=['GET'])
def dashboard():
    # Retrieve the vehicles from the database
    vehicles=VehiclesHandler().get_all_information()
    return render_template('dashboard_index.html',tools=vehicles)

@PageRoutes.route('/vehicle_details', methods=['GET'])
def vehicle_details():
    return render_template('vehicle_details.html')
