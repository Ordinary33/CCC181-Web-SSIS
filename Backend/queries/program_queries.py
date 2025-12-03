class ProgramQueries:
    SELECT_ALL = "SELECT * FROM programs ORDER BY program_code"
    
    SELECT_BY_CODE = "SELECT * FROM programs WHERE program_code = %s"
    
    CHECK_EXISTS = "SELECT 1 FROM programs WHERE program_code = %s"
    
    INSERT_PROGRAM = """
        INSERT INTO programs (program_code, program_name, college_code)
        VALUES (%s, %s, %s)
        RETURNING *;
    """
    
    UPDATE_PROGRAM = """
        UPDATE programs
        SET program_code = %s, program_name = %s, college_code = %s
        WHERE program_code = %s
        RETURNING *;
    """
    
    DELETE_PROGRAM = "DELETE FROM programs WHERE program_code = %s RETURNING *"