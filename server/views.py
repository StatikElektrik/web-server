"""
This module contains the routes for serving the HTML files.
"""

from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import ProjectManagersHandler, VehiclesHandler, UsersHandler
from functools import wraps

# This route is for serving the HTML files.
PageRoutes = Blueprint("PageRoutes", __name__)


def login_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Please log in to access this page.")
            return redirect(url_for('PageRoutes.login'))
        return route_function(*args, **kwargs)
    return decorated_function


@PageRoutes.route("/", methods=["GET"])
def index():
    """It provides the index page."""
    return render_template("index.html")


@PageRoutes.route("/about-us", methods=["GET"])
def about_us():
    """It provides the about us page."""
    # Retrieve the project managers from the database.
    project_managers = ProjectManagersHandler().get_all_information()
    return render_template("about_us.html", members=project_managers)


@PageRoutes.route("/project_details", methods=["GET"])
def project_details():
    """It provides the project details page."""
    return render_template("project_details.html")


@PageRoutes.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """It provides the dashboard page."""
    # Retrieve the vehicles from the database
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    vehicles = VehiclesHandler().get_all_information()
    return render_template("dashboard_index.html", tools=vehicles)


@PageRoutes.route("/vehicle_details", methods=["GET"])
def vehicle_details():
    """It provides the vehicle details page."""
    return render_template("vehicle_details.html")


@PageRoutes.route("/login", methods=["GET", "POST"])
def login():
    """It provides the login page."""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = UsersHandler()
        user_exist = user.check_email(email)
        if not user_exist or not check_password_hash(
            user.get_hash_password(email), password
        ):
            flash("Please check your login details and try again.")
            return redirect(url_for("PageRoutes.login"))
        else:
            session['logged_in'] = True
            return redirect(url_for("PageRoutes.dashboard"))
    else:
        return render_template("auth/login.html")


@PageRoutes.route("/signup", methods=["GET", "POST"])
def signup():
    """It provides the signup page."""
    if request.method == "POST":
        name_surname = request.form["name_surname"]
        company = request.form["company"]
        email = request.form["email"]
        password = request.form["password"]
        password = generate_password_hash(password, method="sha256")
        User = UsersHandler()

        # if this returns a user, then the email already exists
        user_exist = User.check_email(email)
        if user_exist:  # if a user exist
            flash("Email address already exists")
            return redirect(url_for("PageRoutes.signup"))
        else:
            new_user = [name_surname, company, email, password]
            User.register_user(new_user)
            flash("User registered successfully!")
            return redirect(url_for("PageRoutes.login"))
    else:
        return render_template("auth/signup.html")


@PageRoutes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('PageRoutes.login'))
