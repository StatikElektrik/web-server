"""
This module contains the API routes for the
server. These routes are responsible for
serving the REST/CoAP API endpoints and their
associated logic.
"""

from flask import Blueprint
from flask import jsonify

from analysis import PredictiveMaintainance
from database import ProjectManagersHandler

ApiRoutes = Blueprint("ApiRoutes", __name__, url_prefix="/api")


@ApiRoutes.route("/hello-world", methods=["GET"])
def hello_world():
    """A simple hello world endpoint."""
    return jsonify({"message": PredictiveMaintainance.hello_world()})


@ApiRoutes.route("/people", methods=["GET"])
def get_people():
    """Get the names of all people in the database."""
    return jsonify({"people": ProjectManagersHandler().get_names()})
