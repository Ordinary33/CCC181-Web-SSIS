from psycopg.rows import dict_row
from db import get_pool
from queries.student_queries import StudentQueries

class StudentRepository:
    def __init__(self):
        self.pool = get_pool()

    def get_all(self):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(StudentQueries.SELECT_ALL)
                return cur.fetchall()

    def get_by_id(self, student_id):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(StudentQueries.SELECT_BY_ID, (student_id,))
                return cur.fetchone()
            
    def get_paginated(self, search_term, filter_field, sort_column, sort_dir, limit, offset):
        """
        filter_field: The specific DB column to search (e.g., 'first_name') or 'all'
        sort_column: The DB column to sort by (e.g., 'student_id')
        sort_dir: 'ASC' or 'DESC'
        """
        
        sql_where = ""
        params = []

        if search_term:
            term = f"%{search_term}%"
            
            if filter_field == 'all':

                sql_where = """
                    WHERE student_id ILIKE %s 
                    OR first_name ILIKE %s 
                    OR last_name ILIKE %s 
                    OR year_level::text ILIKE %s 
                    OR gender ILIKE %s 
                    OR program_code ILIKE %s
                """

                params = [term] * 6 
            else:

                sql_where = f"WHERE {filter_field}::text ILIKE %s"
                params = [term]

        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:

                count_query = f"{StudentQueries.COUNT_BASE} {sql_where}"
                cur.execute(count_query, params)
                total_records = cur.fetchone()['count']

                data_query = f"""
                    {StudentQueries.SELECT_BASE} 
                    {sql_where}
                    ORDER BY {sort_column} {sort_dir}
                    LIMIT %s OFFSET %s
                """
                
                final_params = params + [limit, offset]
                
                cur.execute(data_query, final_params)
                students = cur.fetchall()

                return students, total_records

    def exists(self, student_id):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(StudentQueries.CHECK_EXISTS, (student_id,))
                return cur.fetchone() is not None

    def create(self, data):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(StudentQueries.INSERT_STUDENT, (
                    data["student_id"], data["first_name"], data["last_name"],
                    data["year_level"], data["gender"], data["program_code"]
                ))
                new_student = cur.fetchone()
                conn.commit()
                return new_student

    def update(self, current_id, data):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(StudentQueries.UPDATE_STUDENT, (
                    data["student_id"], data["first_name"], data["last_name"],
                    data["year_level"], data["gender"], data["program_code"],
                    current_id  # The ID used in the WHERE clause
                ))
                updated = cur.fetchone()
                conn.commit()
                return updated

    def update_image(self, student_id, image_url):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(StudentQueries.UPDATE_IMAGE, (image_url, student_id))
                updated = cur.fetchone()
                conn.commit()
                return updated

    def delete(self, student_id):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(StudentQueries.DELETE_STUDENT, (student_id,))
                deleted = cur.fetchone()
                conn.commit()
                return deleted