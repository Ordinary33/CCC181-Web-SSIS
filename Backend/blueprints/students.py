from flask import Blueprint, request, jsonify
from psycopg.rows import dict_row
from db import get_pool


students_bp = Blueprint("students", __name__)


REQUIRED_FIELDS = ["student_id", "first_name", "last_name", "year_level", "gender", "program_code"]




@students_bp.route("/", methods=["GET"])
def list_students():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM students ORDER BY student_id")
            rows = cur.fetchall()
    return jsonify(rows), 200




@students_bp.route("/", methods=["POST"])
def create_student():
    data = request.get_json() or {}
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




@students_bp.route("/<student_id>", methods=["PUT"])
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




@students_bp.route("/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 1 FROM students WHERE student_id = %s",
            (student_id,))
            if not cur.fetchone():
                return jsonify({"error": "Student not found"}), 404
            cur.execute("DELETE FROM students WHERE student_id = %s RETURNING *", (student_id,))
            deleted = cur.fetchone()
        conn.commit()
    return jsonify({"message": "Student deleted successfully", "student":
    deleted}), 200
