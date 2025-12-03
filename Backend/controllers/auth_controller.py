from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from services.auth_service import AuthService

auth_service = AuthService()

def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    response, status_code = auth_service.register_user(username, password)
    return jsonify(response), status_code

def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    response, status_code = auth_service.login_user(username, password)
    return jsonify(response), status_code

def protected_route():
    current_user_id = get_jwt_identity()
    return jsonify({"message": f"Hello user {current_user_id}"}), 200