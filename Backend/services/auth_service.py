from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from repository.auth_repo import UserRepository

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, username, password):
        # 1. Check if user already exists
        existing_user = self.user_repo.get_by_username(username)
        if existing_user:
            return {"error": "Username already exists"}, 400

        # 2. Hash password
        hashed_pw = generate_password_hash(password)

        # 3. Save to DB
        user_id = self.user_repo.create(username, hashed_pw)
        
        return {"message": "Account created", "user_id": user_id}, 201

    def login_user(self, username, password):
        # 1. Get user from DB
        user_row = self.user_repo.get_by_username(username)
        
        # 2. Validate password
        if user_row and check_password_hash(user_row[1], password):
            user_id = user_row[0]
            access_token = create_access_token(identity=str(user_id))
            return {"access_token": access_token}, 200
            
        return {"error": "Invalid username or password"}, 401