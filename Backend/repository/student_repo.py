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
            
    def get_paginated(self, search_term, filter_field, sort_column, sort_dir, limit, offset, program_filter=None, year_filter=None, gender_filter=None, college_filter=None):
        sql_where = []
        params = []

        if search_term:
            term = f"%{search_term}%"
            if filter_field == 'all':
                sql_where.append("""
                    (student_id ILIKE %s 
                    OR s.first_name ILIKE %s 
                    OR s.last_name ILIKE %s 
                    OR s.year_level::text ILIKE %s 
                    OR s.gender ILIKE %s 
                    OR s.program_code ILIKE %s
                    OR p.college_code ILIKE %s)
                """)
                params.extend([term] * 7)
            else:
                sql_where.append(f"{filter_field}::text ILIKE %s")
                params.append(term)

        if program_filter:
            sql_where.append("s.program_code = %s")
            params.append(program_filter)

        if year_filter:
            sql_where.append("s.year_level = %s")
            params.append(year_filter)

        if gender_filter:
            sql_where.append("s.gender = %s")
            params.append(gender_filter)
            
        if college_filter:
            sql_where.append("p.college_code = %s") 
            params.append(college_filter)

        where_clause = ""
        if sql_where:
            where_clause = "WHERE " + " AND ".join(sql_where)

        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                count_query = f"{StudentQueries.COUNT_BASE} {where_clause}"
                cur.execute(count_query, params)
                total_records = cur.fetchone()['count']

                data_query = f"""
                    {StudentQueries.SELECT_BASE} 
                    {where_clause}
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
                    current_id  
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