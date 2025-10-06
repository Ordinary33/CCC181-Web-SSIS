from flask import Blueprint, request, jsonify
from psycopg.rows import dict_row
from db import get_pool
from flask_jwt_extended import jwt_required
from flask_cors import CORS

colleges_bp = Blueprint("colleges", __name__)
CORS(colleges_bp)

REQUIRED_FIELDS = ["college_code", "college_name"]

@colleges_bp.route("/", methods=["GET"], strict_slashes=False)
def list_colleges():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM colleges ORDER BY college_code")
            rows = cur.fetchall()
    return jsonify(rows), 200

@colleges_bp.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_college():
    data = request.get_json() or {}
    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            return jsonify({"error": f"{f} is required"}), 400

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 1 FROM colleges WHERE college_code = %s", (data["college_code"],))
            if cur.fetchone():
                return jsonify({"error": "College Code already exists. Please use a different Code."}), 409

            cur.execute(
                """
                INSERT INTO colleges (college_code, college_name)
                VALUES (%s, %s)
                RETURNING *;
                """,
                (data["college_code"], data["college_name"]),
            )
            new_college = cur.fetchone()
        conn.commit()

    return jsonify({"message": "College created successfully", "college": new_college}), 201

@colleges_bp.route("/<college_code>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_college(college_code):
    data = request.get_json() or {}
    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            return jsonify({"error": f"{f} is required"}), 400

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 1 FROM colleges WHERE college_code = %s", (college_code,))
            if not cur.fetchone():
                return jsonify({"error": "College not found"}), 404

            if data["college_code"] != college_code:
                cur.execute("SELECT 1 FROM colleges WHERE college_code = %s", (data["college_code"],))
                if cur.fetchone():
                    return jsonify({"error": "College Code already exists. Please use a different Code."}), 409

            cur.execute(
                """
                UPDATE colleges
                SET college_code = %s, college_name = %s
                WHERE college_code = %s
                RETURNING *;
                """,
                (data["college_code"], data["college_name"], college_code),
            )
            updated = cur.fetchone()
        conn.commit()

    return jsonify({"message": "College updated successfully", "college": updated}), 200

@colleges_bp.route("/<college_code>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_college(college_code):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 1 FROM colleges WHERE college_code = %s", (college_code,))
            if not cur.fetchone():
                return jsonify({"error": "College not found"}), 404

            cur.execute("DELETE FROM colleges WHERE college_code = %s RETURNING *", (college_code,))
            deleted = cur.fetchone()
        conn.commit()

    return jsonify({"message": "College deleted successfully", "college": deleted}), 200
