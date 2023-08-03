from flask import Blueprint
from flask import jsonify

# This route is for serving the REST/CoAP API
# endpoints and their associated logic.
ApiRoutes = Blueprint('ApiRoutes', __name__, url_prefix='/api')

@ApiRoutes.route('/hello-world', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, world!'})