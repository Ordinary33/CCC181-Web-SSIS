from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os

load_dotenv()

from blueprints.students import students_bp
from blueprints.programs import programs_bp
from blueprints.colleges import colleges_bp
from blueprints.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") 

    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    jwt = JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(students_bp, url_prefix="/students")
    app.register_blueprint(programs_bp, url_prefix="/programs")
    app.register_blueprint(colleges_bp, url_prefix="/colleges")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
