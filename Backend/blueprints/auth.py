from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import get_pool

auth_bp = Blueprint("auth", __name__)
pool = get_pool()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    password_hash = generate_password_hash(password)
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username=%s", (username,))
            if cur.fetchone():
                return jsonify({"error": "Username already exists"}), 400
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id",
                (username, password_hash)
            )
            user_id = cur.fetchone()[0]
            
        conn.commit()

    return jsonify({"message": "Account created", "user_id": user_id}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, password_hash FROM users WHERE username=%s", (username,))
            row = cur.fetchone()

    if row and check_password_hash(row[1], password):
        access_token = create_access_token(identity=str(row[0]))
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid username or password"}), 401


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return jsonify({"message": f"Hello user {user_id}"}), 200
