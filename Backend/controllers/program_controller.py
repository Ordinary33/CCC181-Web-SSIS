from flask import request, jsonify
from services.program_service import ProgramService

program_service = ProgramService()
REQUIRED_FIELDS = ["program_code", "program_name", "college_code"]

def list_programs():
    response, status = program_service.get_all_programs()
    return jsonify(response), status

def get_program(program_code):
    response, status = program_service.get_program(program_code)
    return jsonify(response), status

def create_program():
    data = request.get_json() or {}
    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            return jsonify({"error": f"{f} is required"}), 400
            
    response, status = program_service.create_program(data)
    return jsonify(response), status

def update_program(program_code):
    data = request.get_json() or {}
    for f in REQUIRED_FIELDS:
        if f not in data or data[f] in (None, ""):
            return jsonify({"error": f"{f} is required"}), 400

    response, status = program_service.update_program(program_code, data)
    return jsonify(response), status

def delete_program(program_code):
    response, status = program_service.delete_program(program_code)
    return jsonify(response), status