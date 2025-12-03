from flask import request, jsonify
from services.college_service import CollegeService

college_service = CollegeService()
REQUIRED_FIELDS = ["college_code", "college_name"]

def list_colleges():
    response, status = college_service.get_all_colleges()
    return jsonify(response), status

def get_college(college_code):
    response, status = college_service.get_college(college_code)
    return jsonify(response), status

def create_college():
    data = request.get_json() or {}
    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            return jsonify({"error": f"{f} is required"}), 400
            
    response, status = college_service.create_college(data)
    return jsonify(response), status

def update_college(college_code):
    data = request.get_json() or {}
    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            return jsonify({"error": f"{f} is required"}), 400

    response, status = college_service.update_college(college_code, data)
    return jsonify(response), status

def delete_college(college_code):
    response, status = college_service.delete_college(college_code)
    return jsonify(response), status