class CollegeQueries:
    SELECT_ALL = "SELECT * FROM colleges ORDER BY college_code"
    
    SELECT_BY_CODE = "SELECT * FROM colleges WHERE college_code = %s"
    
    CHECK_EXISTS = "SELECT 1 FROM colleges WHERE college_code = %s"
    
    INSERT_COLLEGE = """
        INSERT INTO colleges (college_code, college_name)
        VALUES (%s, %s)
        RETURNING *;
    """
    
    UPDATE_COLLEGE = """
        UPDATE colleges
        SET college_code = %s, college_name = %s
        WHERE college_code = %s
        RETURNING *;
    """
    
    DELETE_COLLEGE = "DELETE FROM colleges WHERE college_code = %s RETURNING *"