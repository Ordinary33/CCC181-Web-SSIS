from flask import request, jsonify
from services.student_service import StudentService

student_service = StudentService()
REQUIRED_FIELDS = ["student_id", "first_name", "last_name", "year_level", "gender", "program_code"]

def list_students():
    response, status = student_service.get_all_students()
    return jsonify(response), status

def get_student(student_id):
    response, status = student_service.get_student(student_id)
    return jsonify(response), status

def create_student():
    data = request.get_json()
    # Basic Input Validation
    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            return jsonify({"error": f"{f} is required"}), 400
            
    response, status = student_service.create_student(data)
    return jsonify(response), status

def update_student(student_id):
    data = request.get_json() or {}
    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            return jsonify({"error": f"{f} is required"}), 400

    response, status = student_service.update_student(student_id, data)
    return jsonify(response), status

def delete_student(student_id):
    response, status = student_service.delete_student(student_id)
    return jsonify(response), status

def update_student_image(student_id):
    data = request.get_json()
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    response, status = student_service.update_student_image(student_id, image_url)
    return jsonify(response), status