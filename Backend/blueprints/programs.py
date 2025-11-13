from flask import Blueprint, request, jsonify
from psycopg.rows import dict_row
from db import get_pool
from flask_jwt_extended import jwt_required, get_jwt_identity

programs_bp = Blueprint("programs", __name__)
REQUIRED_FIELDS = ["program_code", "program_name", "college_code"]

@programs_bp.route("/", methods=["GET"])
def list_programs():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM programs ORDER BY program_code")
            rows = cur.fetchall()
    return jsonify(rows), 200

@programs_bp.route("/", methods=["POST"])
@jwt_required()
def create_program():
    data = request.get_json() or {}

    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            return jsonify({"error": f"{f} is required"}), 400

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 1 FROM programs WHERE program_code = %s", (data["program_code"],))
            if cur.fetchone():
                return jsonify({"error": "Program Code already exists. Please use a different Code."}), 409

            cur.execute(
                """
                INSERT INTO programs (program_code, program_name, college_code)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (data["program_code"], data["program_name"], data["college_code"]),
            )
            new = cur.fetchone()
        conn.commit()

    return jsonify({"message": "Program created successfully", "program": new}), 201

@programs_bp.route("/<program_code>", methods=["PUT"])
@jwt_required()
def update_program(program_code):
    data = request.get_json() or {}

    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            return jsonify({"error": f"{f} is required"}), 400

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 1 FROM programs WHERE program_code = %s", (program_code,))
            if not cur.fetchone():
                return jsonify({"error": "Program not found"}), 404

            if data["program_code"] != program_code:
                cur.execute("SELECT 1 FROM programs WHERE program_code = %s", (data["program_code"],))
                if cur.fetchone():
                    return jsonify({"error": "Program Code already exists. Please use a different Code."}), 409

            cur.execute(
                """
                UPDATE programs
                SET program_code = %s, program_name = %s, college_code = %s
                WHERE program_code = %s
                RETURNING *;
                """,
                (
                    data["program_code"],
                    data["program_name"],
                    data["college_code"],
                    program_code,
                ),
            )
            updated = cur.fetchone()
        conn.commit()

    return jsonify({"message": "Program updated successfully", "program": updated}), 200

@programs_bp.route("/<program_code>", methods=["DELETE"])
@jwt_required()
def delete_program(program_code):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 1 FROM programs WHERE program_code = %s", (program_code,))
            if not cur.fetchone():
                return jsonify({"error": "Program not found"}), 404

            cur.execute("DELETE FROM programs WHERE program_code = %s RETURNING *", (program_code,))
            deleted = cur.fetchone()
        conn.commit()

    return jsonify({"message": "Program deleted successfully", "program": deleted}), 200

@programs_bp.route("/<program_code>", methods=["GET"])
def get_program(program_code):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM programs WHERE program_code = %s", (program_code,))
            program = cur.fetchone()

    if not program:
        return jsonify({"error": "Program not found"}), 404

    return jsonify(program), 200
