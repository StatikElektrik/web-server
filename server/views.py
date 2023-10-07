from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash

from database import ProjectManagersHandler,VehiclesHandler, UsersHandler, DatabaseHandler
from database.DatabaseHandler import create_database_handler
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

###############   AUTHENTICATION METHODS  #####################
@PageRoutes.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')

@PageRoutes.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        user_data = {
        'COLUMN_NAME': request.form['name_surname'],
        'COLUMN_COMP': request.form['company'],
        'COLUMN_MAIL': request.form['email'],
        'COLUMN_PASSWORD': request.form['password']
    }
        print(user_data)
        veri=create_database_handler()
        veri.insert_into_table('Users', user_data)
        return redirect(url_for("PageRoutes.login"))
    else:
        return render_template('auth/signup.html')

    


