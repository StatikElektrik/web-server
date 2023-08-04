from flask import Blueprint
from flask import jsonify

from analysis import AnalysisUtils, PredictiveMaintainance
from database import ProjectManagersHandler

# This route is for serving the REST/CoAP API
# endpoints and their associated logic.
ApiRoutes = Blueprint("ApiRoutes", __name__, url_prefix="/api")


@ApiRoutes.route("/hello-world", methods=["GET"])
def hello_world():
    return jsonify({"message": PredictiveMaintainance.hello_world()})


@ApiRoutes.route("/people", methods=["GET"])
def get_people():
    return jsonify({"people": ProjectManagersHandler().get_names()})
