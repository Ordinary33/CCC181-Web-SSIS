from repository.program_repo import ProgramRepository

class ProgramService:
    def __init__(self):
        self.repo = ProgramRepository()

    def get_all_programs(self):
        return self.repo.get_all(), 200

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