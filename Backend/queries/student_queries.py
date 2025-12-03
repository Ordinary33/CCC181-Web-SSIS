class StudentQueries:
    SELECT_BASE = "SELECT * FROM students"
    COUNT_BASE = "SELECT COUNT(*) AS count FROM students"
    
    SELECT_ALL = "SELECT * FROM students ORDER BY student_id"
    
    SELECT_BY_ID = "SELECT * FROM students WHERE student_id = %s"
    
    CHECK_EXISTS = "SELECT 1 FROM students WHERE student_id = %s"
    
    INSERT_STUDENT = """
        INSERT INTO students (student_id, first_name, last_name, year_level, gender, program_code)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *;
    """
    
    UPDATE_STUDENT = """
        UPDATE students
        SET student_id = %s, first_name = %s, last_name = %s, year_level = %s, gender = %s, program_code = %s
        WHERE student_id = %s
        RETURNING *;
    """
    
    UPDATE_IMAGE = "UPDATE students SET image_url = %s WHERE student_id = %s RETURNING *"
    
    DELETE_STUDENT = "DELETE FROM students WHERE student_id = %s RETURNING *"