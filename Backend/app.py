from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()


from blueprints.students import students_bp
from blueprints.programs import programs_bp
from blueprints.colleges import colleges_bp




def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(students_bp, url_prefix="/students")
    app.register_blueprint(programs_bp, url_prefix="/programs")
    app.register_blueprint(colleges_bp, url_prefix="/colleges")
    return app




app = create_app()


if __name__ == "__main__":
    app.run(debug=True)