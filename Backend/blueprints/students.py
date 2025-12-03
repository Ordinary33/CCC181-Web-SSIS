from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_cors import CORS
from controllers import student_controller

students_bp = Blueprint("students", __name__)
CORS(students_bp)

@students_bp.route("/", methods=["GET"], strict_slashes=False)
def list_students():
    return student_controller.list_students()

@students_bp.route("/<student_id>", methods=["GET"], strict_slashes=False)
def get_student(student_id):
    return student_controller.get_student(student_id)

@students_bp.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_student():
    return student_controller.create_student()

@students_bp.route("/<student_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_student(student_id):
    return student_controller.update_student(student_id)

@students_bp.route("/<student_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_student(student_id):
    return student_controller.delete_student(student_id)

@students_bp.route("/<student_id>/image", methods=["PATCH"], strict_slashes=False)
@jwt_required()
def update_student_image(student_id):
    return student_controller.update_student_image(student_id)