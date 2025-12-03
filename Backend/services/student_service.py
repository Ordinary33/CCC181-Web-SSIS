from repository.student_repo import StudentRepository

class StudentService:
    def __init__(self):
        self.repo = StudentRepository()

    def get_all_students(self):
        return self.repo.get_all(), 200

    def get_student(self, student_id):
        student = self.repo.get_by_id(student_id)
        if not student:
            return {"error": "Student not found"}, 404
        return student, 200

    def create_student(self, data):
        if self.repo.exists(data["student_id"]):
            return {"error": "Student ID already exists. Please use a different ID."}, 409
        
        new_student = self.repo.create(data)
        return {"message": "Student created successfully", "student": new_student}, 201

    def update_student(self, current_id, data):

        if not self.repo.exists(current_id):
            return {"error": "Student not found"}, 404

        if data["student_id"] != current_id:
            if self.repo.exists(data["student_id"]):
                return {"error": "Student ID already exists. Please use a different ID."}, 409

        updated_student = self.repo.update(current_id, data)
        return {"message": "Student updated successfully", "student": updated_student}, 200

    def delete_student(self, student_id):
        if not self.repo.exists(student_id):
            return {"error": "Student not found"}, 404
            
        deleted_student = self.repo.delete(student_id)
        return {"message": "Student deleted successfully", "student": deleted_student}, 200

    def update_student_image(self, student_id, image_url):
        if not self.repo.exists(student_id):
            return {"error": "Student not found"}, 404
            
        updated_student = self.repo.update_image(student_id, image_url)
        return {"message": "Student image updated successfully", "student": updated_student}, 200