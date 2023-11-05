"""
This module contains the routes for serving the HTML files.
"""
from datetime import datetime
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
            flash({"text": "Please log in to access this page.", "msg_type": "warning"})
            return redirect(url_for("PageRoutes.login"))
        return route_function(*args, **kwargs)

    return decorated_function


@PageRoutes.route("/", methods=["GET"])
def index():
    """It provides the index page."""
    return render_template("index.html", logged_in=session.get("logged_in"))


@PageRoutes.route("/about-us", methods=["GET"])
def about_us():
    """It provides the about us page."""
    # Retrieve the project managers from the database.
    project_managers = ProjectManagersHandler().get_all_information()
    return render_template("about_us.html",
                           members=project_managers,
                           logged_in=session.get("logged_in"))


@PageRoutes.route("/project_details", methods=["GET"])
def project_details():
    """It provides the project details page."""
    return render_template("project_details.html", logged_in=session.get("logged_in"))


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
            flash({"text": "Please check your login details and try again.", "msg_type": "warning"})
            return redirect(url_for("PageRoutes.login"))
        else:
            session["logged_in"] = True
            return redirect(url_for("PageRoutes.dashboard"))

    # If request made with GET, render the login page.
    return render_template("login.html")


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
            flash({"text": "Something went wrong. Please try again.", "msg_type": "warning"})
            return redirect(url_for("PageRoutes.signup"))
        elif result == RegistrationStates.ALREADY_REGISTERED:
            flash({"text": "Email address already exists", "msg_type": "warning"})
            return redirect(url_for("PageRoutes.signup"))
        elif result == RegistrationStates.SUCCESS:
            flash({"text": "User registered successfully!", "msg_type": "primary"})
            return redirect(url_for("PageRoutes.login"))
        else:
            flash({"text": "Something went wrong. Please try again.", "msg_type": "warning"})
            return redirect(url_for("PageRoutes.signup"))
    else:
        return render_template("signup.html")


@PageRoutes.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """It provides the dashboard page."""
    # Retrieve the vehicles from the database
    if not session.get("logged_in"):
        return redirect(url_for("PageRoutes.login"))
    vehicles = VehiclesHandler().get_all_information()
    return render_template("dashboard.html",
                           datatable=vehicles,
                           customer_id="01",
                           company_name="IETT",
                           page_name="Dashboard",
                           summary_information={"total": 86, "planned": 15, "required": 19},
                           suggestions=[
                               "Consider changing M4.56's route with M4.57's route.",
                                "34KLM56 is not in the route. Please check it."
                            ],
                            user_name="John Doe"
                           )


@PageRoutes.route("/details", methods=["GET"])
@login_required
def details():
    """It provides the vehicle details page."""
    query_arguments = request.args.to_dict()
    if not query_arguments:
        flash({"text": "Please select a vehicle to view details.", "msg_type": "warning"})
        return redirect(url_for("PageRoutes.dashboard"))

    vehicle_id = query_arguments["vid"]
    customer_id = query_arguments["cid"]

    selected_vehicle = None
    for vehicle in VehiclesHandler().get_all_information():
        if vehicle["vid"].lower() == vehicle_id.lower():
            selected_vehicle = vehicle
            break

    if not selected_vehicle:
        flash({"text": "Please select a vehicle to view details.", "msg_type": "warning"})
        return redirect(url_for("PageRoutes.dashboard"))

    return render_template("details.html",
        user_name="John Doe",
        company_name="IETT",
        page_name="Vehicle Details",
        image_location="metro_image.png",
        vehicle_details={
            "vehicle_id": vehicle_id,
            "customer_id": customer_id,
            "plate": selected_vehicle.get("plate"),
            "route": selected_vehicle.get("route"),
            "last_date": selected_vehicle.get("last_date"),
            "class": selected_vehicle.get("class"),
            "status": "Active",
            "last_location": f"Longitude: {selected_vehicle.get('gps_longitude')}, "
                             f"Latitude: {selected_vehicle.get('gps_latitude')}",
            "battery": selected_vehicle.get("battery"),
        },
        driver_details={
            "profile_photo": "bus_driver.jpg",
            "name": "John Doe",
            "phone": "+90 532 123 45 67",
        },
        prediction_details={
            "failure_date": "05/11/2023",
            "failure_reason": "Piston corrosion on cyclinder 3",
        },
        back_link="/dashboard",
    )


@PageRoutes.route("/profile", methods=["GET"])
@login_required
def profile():
    """It provides the profile page."""
    return render_template("profile.html",
                           company_name="IETT",
                           page_name="Profile")


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
        last_date = request.form["last_date"]
        last_date = datetime.strptime(last_date, "%Y-%m-%d")

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
            flash({"text": "Something went wrong. Please try again.", "msg_type": "warning"})
            return redirect(url_for("PageRoutes.device_register"))
        elif result == RegistrationStates.ALREADY_REGISTERED:
            flash({"text": "Device already registered.", "msg_type": "warning"})
            return redirect(url_for("PageRoutes.device_register"))
        elif result == RegistrationStates.SUCCESS:
            flash({"text": "Device registered successfully!", "msg_type": "primary"})
            return redirect(url_for("PageRoutes.dashboard"))

    # Render the register page if request made with GET.
    return render_template("register_device.html",
                           company_name="IETT",
                           page_name="Register New Device",
                           user_name="John Doe",
                           vehicle_types=[
                            {"id": 0, "name": "Bus"},
                            {"id": 1, "name": "Tram"},
                            {"id": 2, "name": "Metrobus"},
                            {"id": 3, "name": "Metro"},
                            {"id": 4, "name": "Ferry"},
                            {"id": 5, "name": "Marmaray"},
                            {"id": 7, "name": "Funicular"},
                           ])
