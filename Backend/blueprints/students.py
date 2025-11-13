from flask import Blueprint, request, jsonify
from psycopg.rows import dict_row
from db import get_pool
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS

students_bp = Blueprint("students", __name__)
CORS(students_bp)  # allow all origins for this blueprint

REQUIRED_FIELDS = ["student_id", "first_name", "last_name", "year_level", "gender", "program_code"]

@students_bp.route("/", methods=["GET"], strict_slashes=False)
def list_students():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM students ORDER BY student_id")
            rows = cur.fetchall()
    return jsonify(rows), 200

@students_bp.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_student():
    data = request.get_json()
    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            return jsonify({"error": f"{f} is required"}), 400

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 1 FROM students WHERE student_id = %s", (data["student_id"],))
            if cur.fetchone():
                return jsonify({"error": "Student ID already exists. Please use a different ID."}), 409

            cur.execute(
                """
                INSERT INTO students (student_id, first_name, last_name, year_level, gender, program_code)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (
                    data["student_id"],
                    data["first_name"],
                    data["last_name"],
                    data["year_level"],
                    data["gender"],
                    data["program_code"],
                ),
            )
            new_student = cur.fetchone()
        conn.commit()

    return jsonify({"message": "Student created successfully", "student": new_student}), 201

@students_bp.route("/<student_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_student(student_id):
    data = request.get_json() or {}
    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            return jsonify({"error": f"{f} is required"}), 400

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 1 FROM students WHERE student_id = %s", (student_id,))
            if not cur.fetchone():
                return jsonify({"error": "Student not found"}), 404

            if data["student_id"] != student_id:
                cur.execute("SELECT 1 FROM students WHERE student_id = %s", (data["student_id"],))
                if cur.fetchone():
                    return jsonify({"error": "Student ID already exists. Please use a different ID."}), 409

            cur.execute(
                """
                UPDATE students
                SET student_id = %s, first_name = %s, last_name = %s, year_level = %s, gender = %s, program_code = %s
                WHERE student_id = %s
                RETURNING *;
                """,
                (
                    data["student_id"],
                    data["first_name"],
                    data["last_name"],
                    data["year_level"],
                    data["gender"],
                    data["program_code"],
                    student_id,
                ),
            )
            updated = cur.fetchone()
        conn.commit()

    return jsonify({"message": "Student updated successfully", "student": updated}), 200

@students_bp.route("/<student_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_student(student_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 1 FROM students WHERE student_id = %s", (student_id,))
            if not cur.fetchone():
                return jsonify({"error": "Student not found"}), 404

            cur.execute("DELETE FROM students WHERE student_id = %s RETURNING *", (student_id,))
            deleted = cur.fetchone()
        conn.commit()

    return jsonify({"message": "Student deleted successfully", "student": deleted}), 200

@students_bp.route("/<student_id>/image", methods=["PATCH"], strict_slashes=False)
@jwt_required()
def update_student_image(student_id):
    data = request.get_json()
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 1 FROM students WHERE student_id = %s", (student_id,))
            if not cur.fetchone():
                return jsonify({"error": "Student not found"}), 404

            cur.execute(
                "UPDATE students SET image_url = %s WHERE student_id = %s RETURNING *",
                (image_url, student_id)
            )
            updated_student = cur.fetchone()
        conn.commit()

    return jsonify({"message": "Student image updated successfully", "student": updated_student}), 200
