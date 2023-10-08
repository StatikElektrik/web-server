from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import ProjectManagersHandler,VehiclesHandler, UsersHandler
from flask_login import LoginManager,UserMixin,login_user

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
@PageRoutes.route('/login', methods=['GET','POST'])
def login():
    if request.method =='POST':
        email=request.form['email']
        password=request.form['password']
        remember = True if request.form.get('remember') else False

        User=UsersHandler()
        user_exist = User.check_email(email)
        if not user_exist or not check_password_hash(User.get_hash_password(email), password):
            flash('Please check your login details and try again.')
            return redirect(url_for('PageRoutes.login'))
        else:
            return render_template('dashboard_index.html',user=User)
    else:
        return render_template('auth/login.html')

@PageRoutes.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name_surname=request.form['name_surname']
        company=request.form['company']
        email=request.form['email']
        password=request.form['password']
        password=generate_password_hash(password, method='sha256')
        User=UsersHandler()

        #if this returns a user, then the email already exists
        user_exist = User.check_email(email) 
        if user_exist: # if a user exist
            flash('Email address already exists')
            return redirect(url_for("PageRoutes.signup"))
        else:
            new_user=[name_surname,company,email,password]
            User.register_user(new_user)
            flash('User registered successfully!')
            return redirect(url_for("PageRoutes.login"))
    else:
        return render_template('auth/signup.html')

    


