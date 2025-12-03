from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import program_controller

programs_bp = Blueprint("programs", __name__)

@programs_bp.route("/", methods=["GET"])
def list_programs():
    return program_controller.list_programs()

@programs_bp.route("/", methods=["POST"])
@jwt_required()
def create_program():
    return program_controller.create_program()

@programs_bp.route("/<program_code>", methods=["PUT"])
@jwt_required()
def update_program(program_code):
    return program_controller.update_program(program_code)

@programs_bp.route("/<program_code>", methods=["DELETE"])
@jwt_required()
def delete_program(program_code):
    return program_controller.delete_program(program_code)

@programs_bp.route("/<program_code>", methods=["GET"])
def get_program(program_code):
    return program_controller.get_program(program_code)