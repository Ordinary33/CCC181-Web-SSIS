from repository.student_repo import StudentRepository
import math

class StudentService:
    def __init__(self):
        self.repo = StudentRepository()
        self.COLUMN_MAP = {
            'ID': 'student_id',
            'First Name': 'first_name',
            'Last Name': 'last_name',
            'Year': 'year_level',
            'Gender': 'gender',
            'Program': 'program_code',
            'All': 'all' 
        }

    def get_all_students(self, page, limit, search, filter_by, sort_by, sort_desc, program_filter, year_filter, gender_filter):
        db_filter_field = self.COLUMN_MAP.get(filter_by, 'all')
        db_sort_column = self.COLUMN_MAP.get(sort_by, 'student_id')
        db_sort_dir = "DESC" if sort_desc == 'true' else "ASC"

        offset = (page - 1) * limit

        students, total_records = self.repo.get_paginated(
            search, 
            db_filter_field, 
            db_sort_column, 
            db_sort_dir, 
            limit, 
            offset,
            program_filter,
            year_filter,   
            gender_filter  
        )

        total_pages = math.ceil(total_records / limit) if limit > 0 else 1
        
        return {
            "data": students,
            "pagination": {
                "total_records": total_records,
                "total_pages": total_pages,
                "current_page": page,
                "limit": limit
            }
        }, 200

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
    
    def remove_student_image(self, student_id):
        if not self.repo.exists(student_id):
            return {"error": "Student not found"}, 404
            
        updated_student = self.repo.update_image(student_id, None)
        return {"message": "Student image removed successfully", "student": updated_student}, 200