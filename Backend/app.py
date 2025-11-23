from flask import Flask, send_from_directory, render_template, request
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

load_dotenv()

from blueprints.students import students_bp
from blueprints.programs import programs_bp
from blueprints.colleges import colleges_bp
from blueprints.auth import auth_bp

def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DIST_DIR = os.path.join(BASE_DIR, 'dist')

    app = Flask(
        __name__, 
        static_folder=DIST_DIR, 
        template_folder=DIST_DIR
    )
    
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
    

    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5000",
        "http://localhost:5000"
    ]

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": allowed_origins,
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True
            }
        }
    )

    jwt = JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(students_bp, url_prefix="/api/students")
    app.register_blueprint(programs_bp, url_prefix="/api/programs")
    app.register_blueprint(colleges_bp, url_prefix="/api/colleges")

    @app.before_request
    def spa_history_mode_fallback():
        if request.method != "GET":
            return None

        accept_header = request.headers.get("Accept", "")

        if "text/html" not in accept_header:
            return None

        if request.path.startswith("/api/"):
            return None
        
        return render_template("index.html")
    
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_vue(path):
        if path != "":
            file_path = os.path.join(app.root_path, app.static_folder, path)
            if os.path.exists(file_path) and not os.path.isdir(file_path):
                return send_from_directory(app.static_folder, path)

        return render_template("index.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)