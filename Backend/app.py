import os
from flask import Flask
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

@app.route('/students')
def get_students():
    response = supabase_extension.client.from_('students').select('*').execute()
    return jsonify(response.data)
 
@app.route('/programs')
def get_programs():
    response = supabase_extension.client.from_('programs').select('*').execute()
    return jsonify(response.data)
 
@app.route('/colleges')
def get_colleges():
    response = supabase_extension.client.from_('colleges').select('*').execute()
    return jsonify(response.data)
 
if __name__ == "__main__":
    app.run(debug=True)
                    