class AuthQueries:
    GET_USER_BY_USERNAME = """
        SELECT id, password_hash 
        FROM users 
        WHERE username = %s
    """

    INSERT_USER = """
        INSERT INTO users (username, password_hash) 
        VALUES (%s, %s) 
        RETURNING id
    """