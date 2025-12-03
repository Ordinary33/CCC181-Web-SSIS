from repository.program_repo import ProgramRepository
import math

class ProgramService:
    def __init__(self):
        self.repo = ProgramRepository()
        
        self.COLUMN_MAP = {
            'Program Code': 'program_code',
            'Program Name': 'program_name',
            'College Code': 'college_code',
            'All': 'all'
        }

    def get_all_programs(self, page, limit, search, filter_by, sort_by, sort_desc):
        db_filter_field = self.COLUMN_MAP.get(filter_by, 'all')
        db_sort_column = self.COLUMN_MAP.get(sort_by, 'program_code')
        db_sort_dir = "DESC" if sort_desc == 'true' else "ASC"

        offset = (page - 1) * limit

        programs, total_records = self.repo.get_paginated(
            search, 
            db_filter_field, 
            db_sort_column, 
            db_sort_dir, 
            limit, 
            offset
        )

        total_pages = math.ceil(total_records / limit) if limit > 0 else 1
        
        return {
            "data": programs,
            "pagination": {
                "total_records": total_records,
                "total_pages": total_pages,
                "current_page": page,
                "limit": limit
            }
        }, 200

    def get_program(self, program_code):
        program = self.repo.get_by_code(program_code)
        if not program:
            return {"error": "Program not found"}, 404
        return program, 200

    def create_program(self, data):
        if self.repo.exists(data["program_code"]):
            return {"error": "Program Code already exists. Please use a different Code."}, 409
        
        new_program = self.repo.create(data)
        return {"message": "Program created successfully", "program": new_program}, 201

    def update_program(self, current_code, data):
        if not self.repo.exists(current_code):
            return {"error": "Program not found"}, 404

        if data["program_code"] != current_code:
            if self.repo.exists(data["program_code"]):
                return {"error": "Program Code already exists. Please use a different Code."}, 409

        updated_program = self.repo.update(current_code, data)
        return {"message": "Program updated successfully", "program": updated_program}, 200

    def delete_program(self, program_code):
        if not self.repo.exists(program_code):
            return {"error": "Program not found"}, 404
            
        deleted_program = self.repo.delete(program_code)
        return {"message": "Program deleted successfully", "program": deleted_program}, 200