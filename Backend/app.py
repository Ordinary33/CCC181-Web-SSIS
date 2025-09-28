import os
from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
from flask_supabase import Supabase
from dotenv import load_dotenv

load_dotenv()

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SUPABASE_URL'] = SUPABASE_PROJECT_URL
app.config['SUPABASE_KEY'] = SUPABASE_API_KEY
supabase_extension = Supabase(app)

CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/test")
def test():
    message = "This is a test!"
    return jsonify(message)

@app.route('/students', methods=['GET'])
def get_students():
    response = supabase_extension.client.from_('students').select('*').execute()
    return jsonify(response.data)

@app.route('/students', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        
        required_fields = ['student_id', 'first_name', 'last_name', 'year_level', 'gender', 'program_code']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        existing_student = supabase_extension.client.from_('students').select('student_id').eq('student_id', data['student_id']).execute()
        
        print(f"Checking for duplicate ID: {data['student_id']}")
        print(f"Existing students found: {existing_student.data}")
        
        if existing_student.data:
            print(f"Duplicate found! Returning 409 error")
            return jsonify({'error': 'Student ID already exists. Please use a different ID.'}), 409
        
        response = supabase_extension.client.from_('students').insert(data).execute()
        
        if response.data:
            return jsonify({
                'message': 'Student created successfully',
                'student': response.data[0]
            }), 201
        else:
            return jsonify({'error': 'Failed to create student'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
@app.route('/programs')
def get_programs():
    response = supabase_extension.client.from_('programs').select('*').execute()
    return jsonify(response.data)

@app.route('/programs', methods=['POST'])
def create_program():
    try:
        data = request.get_json()
        
        required_fields = ['program_code', 'program_name', 'college_code']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        existing_program = supabase_extension.client.from_('programs').select('program_code').eq('program_code', data['program_code']).execute()
        
        print(f"Checking for duplicate Code: {data['program_code']}")
        print(f"Existing programs found: {existing_program.data}")
        
        if existing_program.data:
            print(f"Duplicate found! Returning 409 error")
            return jsonify({'error': 'Program Code already exists. Please use a different Code.'}), 409
        
        response = supabase_extension.client.from_('programs').insert(data).execute()
 
        if response.data:
            return jsonify({
                'message': 'Program created successfully',
                'program': response.data[0]
            }), 201
        else:
            return jsonify({'error': 'Failed to create program'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/colleges')
def get_colleges():
    response = supabase_extension.client.from_('colleges').select('*').execute()
    return jsonify(response.data)
 
if __name__ == "__main__":
    app.run(debug=True)
                    