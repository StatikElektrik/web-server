"""
This module contains the routes for serving the HTML files.
"""

from functools import wraps
from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import ProjectManagersHandler, VehiclesHandler, UsersHandler
from database import RegistrationStates

# This route is for serving the HTML files.
PageRoutes = Blueprint("PageRoutes", __name__)


def login_required(route_function):
    """It is a decorator that checks if the user is logged in."""

    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please log in to access this page.")
            return redirect(url_for("PageRoutes.login"))
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


@PageRoutes.route("/login", methods=["GET", "POST"])
def login():
    """It provides the login page."""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = UsersHandler()
        user_exist = user.check_email(email)
        if not user_exist or not check_password_hash(
            user.get_password_hash(email), password
        ):
            flash("Please check your login details and try again.")
            return redirect(url_for("PageRoutes.login"))
        else:
            session["logged_in"] = True
            return redirect(url_for("PageRoutes.dashboard"))

    # If request made with GET, render the login page.
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
        users_handler = UsersHandler()

        result = users_handler.register_user(
            {
                "name_surname": name_surname,
                "company": company,
                "email": email,
                "password": password,
            }
        )

        if result == RegistrationStates.NOT_REGISTERED:
            flash("Something went wrong. Please try again.")
            return redirect(url_for("PageRoutes.signup"))
        elif result == RegistrationStates.ALREADY_REGISTERED:
            flash("Email address already exists")
            return redirect(url_for("PageRoutes.signup"))
        elif result == RegistrationStates.SUCCESS:
            flash("User registered successfully!")
            return redirect(url_for("PageRoutes.login"))
        else:
            flash("Something went wrong. Please try again.")
            return redirect(url_for("PageRoutes.signup"))
    else:
        return render_template("auth/signup.html")


@PageRoutes.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """It provides the dashboard page."""
    # Retrieve the vehicles from the database
    if not session.get("logged_in"):
        return redirect(url_for("PageRoutes.login"))
    vehicles = VehiclesHandler().get_all_information()
    return render_template("dashboard_index.html", tools=vehicles)


@PageRoutes.route("/view_details", methods=["GET"])
@login_required
def view_details():
    """It provides the vehicle details page."""
    return render_template("dashboard/view_details.html")


@PageRoutes.route("/profile", methods=["GET"])
@login_required
def profile():
    """It provides the profile page."""
    return render_template("dashboard/profile.html")


@PageRoutes.route("/logout")
@login_required
def logout():
    """It provides the logout page."""
    session.clear()
    return redirect(url_for("PageRoutes.login"))


@PageRoutes.route("/devices/register", methods=["GET", "POST"])
@login_required
def device_register():
    """It provides the device register page."""
    if request.method == "POST":
        # If not logged in, redirect to login page.
        if not session.get("logged_in"):
            return redirect(url_for("login"))

        device_id = request.form["device_id"]
        vehicle_type = request.form["vehicle_type"]
        plate = request.form["plate"]
        route = request.form["route"]


        vehicles_handler = VehiclesHandler()
        result = vehicles_handler.register_device(
            {
                "device_id": device_id,
                "class": vehicle_type,
                "plate": plate,
                "route": route,
                "last_date": last_date,
            }
        )

        if result == RegistrationStates.NOT_REGISTERED:
            flash("Something went wrong. Please try again.")
            return redirect(url_for("PageRoutes.device_register"))
        elif result == RegistrationStates.ALREADY_REGISTERED:
            flash("Device already registered.")
            return redirect(url_for("PageRoutes.device_register"))
        elif result == RegistrationStates.SUCCESS:
            flash("Device registered successfully!")
            return redirect(url_for("PageRoutes.dashboard"))

    # Render the register page if request made with GET.
    return render_template("register_device.html")
