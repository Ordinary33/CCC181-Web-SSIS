from flask import request, jsonify
from services.student_service import StudentService

student_service = StudentService()
REQUIRED_FIELDS = ["student_id", "first_name", "last_name", "year_level", "gender", "program_code"]

def list_students():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    query = request.args.get("query", "", type=str)
    filter_by = request.args.get("filterBy", "All", type=str)
    sort_by = request.args.get("sortBy", "ID", type=str)
    sort_desc = request.args.get("sortDesc", "false").lower()
    
    program_filter = request.args.get("program", "", type=str)
    year_filter = request.args.get("year", "", type=str)
    gender_filter = request.args.get("gender", "", type=str)
    college_filter = request.args.get("college", "", type=str)


    print(f"DEBUG: Filtering by Year: '{year_filter}', Program: '{program_filter}', Gender: '{gender_filter}', College: '{college_filter}'")
    
    response, status = student_service.get_all_students(
        page, limit, query, filter_by, sort_by, sort_desc, 
        program_filter, year_filter, gender_filter, college_filter
    )
    
    return jsonify(response), status

def get_student(student_id):
    response, status = student_service.get_student(student_id)
    return jsonify(response), status

def create_student():
    data = request.get_json()
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

def delete_student_image(student_id):
    response, status = student_service.remove_student_image(student_id)
    return jsonify(response), status