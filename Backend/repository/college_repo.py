from psycopg.rows import dict_row
from db import get_pool
from queries.college_queries import CollegeQueries

class CollegeRepository:
    def __init__(self):
        self.pool = get_pool()

    def get_paginated(self, search_term, filter_field, sort_column, sort_dir, limit, offset):
        sql_where = ""
        params = []

        if search_term:
            term = f"%{search_term}%"
            
            if filter_field == 'all':
                sql_where = """
                    WHERE college_code ILIKE %s 
                    OR college_name ILIKE %s
                """
                params = [term] * 2
            else:
                sql_where = f"WHERE {filter_field}::text ILIKE %s"
                params = [term]

        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                count_query = f"{CollegeQueries.COUNT_BASE} {sql_where}"
                cur.execute(count_query, params)
                total_records = cur.fetchone()['count']

                data_query = f"""
                    {CollegeQueries.SELECT_BASE} 
                    {sql_where}
                    ORDER BY {sort_column} {sort_dir}
                    LIMIT %s OFFSET %s
                """
                
                final_params = params + [limit, offset]
                
                cur.execute(data_query, final_params)
                colleges = cur.fetchall()

                return colleges, total_records

    def get_by_code(self, college_code):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(CollegeQueries.SELECT_BY_CODE, (college_code,))
                return cur.fetchone()

    def exists(self, college_code):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(CollegeQueries.CHECK_EXISTS, (college_code,))
                return cur.fetchone() is not None

    def create(self, data):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(CollegeQueries.INSERT_COLLEGE, (
                    data["college_code"], 
                    data["college_name"]
                ))
                new_college = cur.fetchone()
                conn.commit()
                return new_college

    def update(self, current_code, data):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(CollegeQueries.UPDATE_COLLEGE, (
                    data["college_code"], 
                    data["college_name"],
                    current_code
                ))
                updated = cur.fetchone()
                conn.commit()
                return updated

    def delete(self, college_code):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(CollegeQueries.DELETE_COLLEGE, (college_code,))
                deleted = cur.fetchone()
                conn.commit()
                return deleted