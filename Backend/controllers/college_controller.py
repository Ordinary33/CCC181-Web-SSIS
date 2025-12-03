from flask import request, jsonify
from services.college_service import CollegeService

college_service = CollegeService()
REQUIRED_FIELDS = ["college_code", "college_name"]

def list_colleges():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    query = request.args.get("query", "", type=str)
    filter_by = request.args.get("filterBy", "All", type=str)
    sort_by = request.args.get("sortBy", "College Code", type=str)
    sort_desc = request.args.get("sortDesc", "false").lower()

    response, status = college_service.get_all_colleges(
        page, limit, query, filter_by, sort_by, sort_desc
    )
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