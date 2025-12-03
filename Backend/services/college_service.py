from repository.college_repo import CollegeRepository
import math

class CollegeService:
    def __init__(self):
        self.repo = CollegeRepository()
        self.COLUMN_MAP = {
            'College Code': 'college_code',
            'College Name': 'college_name',
            'All': 'all'
        }

    def get_all_colleges(self, page, limit, search, filter_by, sort_by, sort_desc):
        db_filter_field = self.COLUMN_MAP.get(filter_by, 'all')
        db_sort_column = self.COLUMN_MAP.get(sort_by, 'college_code')
        db_sort_dir = "DESC" if sort_desc == 'true' else "ASC"

        offset = (page - 1) * limit

        colleges, total_records = self.repo.get_paginated(
            search, 
            db_filter_field, 
            db_sort_column, 
            db_sort_dir, 
            limit, 
            offset
        )

        total_pages = math.ceil(total_records / limit) if limit > 0 else 1
        
        return {
            "data": colleges,
            "pagination": {
                "total_records": total_records,
                "total_pages": total_pages,
                "current_page": page,
                "limit": limit
            }
        }, 200

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