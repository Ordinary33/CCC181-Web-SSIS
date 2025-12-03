from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import auth_controller

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    return auth_controller.register()

@auth_bp.route("/login", methods=["POST"])
def login():
    return auth_controller.login()

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return auth_controller.protected_route()