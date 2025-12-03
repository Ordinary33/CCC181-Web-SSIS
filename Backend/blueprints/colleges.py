from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_cors import CORS
from controllers import college_controller

colleges_bp = Blueprint("colleges", __name__)
CORS(colleges_bp)

@colleges_bp.route("/", methods=["GET"], strict_slashes=False)
def list_colleges():
    return college_controller.list_colleges()

@colleges_bp.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_college():
    return college_controller.create_college()

@colleges_bp.route("/<college_code>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_college(college_code):
    return college_controller.update_college(college_code)

@colleges_bp.route("/<college_code>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_college(college_code):
    return college_controller.delete_college(college_code)

@colleges_bp.route("/<college_code>", methods=["GET"], strict_slashes=False)
def get_college(college_code):
    return college_controller.get_college(college_code)