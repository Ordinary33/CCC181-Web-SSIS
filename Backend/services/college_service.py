from repository.college_repo import CollegeRepository

class CollegeService:
    def __init__(self):
        self.repo = CollegeRepository()

    def get_all_colleges(self):
        return self.repo.get_all(), 200

    def get_college(self, college_code):
        college = self.repo.get_by_code(college_code)
        if not college:
            return {"error": "College not found"}, 404
        return college, 200

    def create_college(self, data):
        if self.repo.exists(data["college_code"]):
            return {"error": "College Code already exists. Please use a different Code."}, 409
        
        new_college = self.repo.create(data)
        return {"message": "College created successfully", "college": new_college}, 201

    def update_college(self, current_code, data):
        if not self.repo.exists(current_code):
            return {"error": "College not found"}, 404

        if data["college_code"] != current_code:
            if self.repo.exists(data["college_code"]):
                return {"error": "College Code already exists. Please use a different Code."}, 409

        updated_college = self.repo.update(current_code, data)
        return {"message": "College updated successfully", "college": updated_college}, 200

    def delete_college(self, college_code):
        if not self.repo.exists(college_code):
            return {"error": "College not found"}, 404
            
        deleted_college = self.repo.delete(college_code)
        return {"message": "College deleted successfully", "college": deleted_college}, 200