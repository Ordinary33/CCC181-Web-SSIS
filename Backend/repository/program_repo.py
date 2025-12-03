from psycopg.rows import dict_row
from db import get_pool
from queries.program_queries import ProgramQueries

class ProgramRepository:
    def __init__(self):
        self.pool = get_pool()
        
    def get_paginated(self, search_term, filter_field, sort_column, sort_dir, limit, offset):
        sql_where = ""
        params = []

        if search_term:
            term = f"%{search_term}%"
            
            if filter_field == 'all':
                sql_where = """
                    WHERE program_code ILIKE %s 
                    OR program_name ILIKE %s 
                    OR college_code ILIKE %s
                """
                params = [term] * 3
            else:
                sql_where = f"WHERE {filter_field}::text ILIKE %s"
                params = [term]

        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                count_query = f"{ProgramQueries.COUNT_BASE} {sql_where}"
                cur.execute(count_query, params)
                total_records = cur.fetchone()['count']

                data_query = f"""
                    {ProgramQueries.SELECT_BASE} 
                    {sql_where}
                    ORDER BY {sort_column} {sort_dir}
                    LIMIT %s OFFSET %s
                """
                
                final_params = params + [limit, offset]
                
                cur.execute(data_query, final_params)
                programs = cur.fetchall()
                
                return programs, total_records

    def get_all(self):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(ProgramQueries.SELECT_ALL)
                return cur.fetchall()

    def get_by_code(self, program_code):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(ProgramQueries.SELECT_BY_CODE, (program_code,))
                return cur.fetchone()

    def exists(self, program_code):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(ProgramQueries.CHECK_EXISTS, (program_code,))
                return cur.fetchone() is not None

    def create(self, data):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(ProgramQueries.INSERT_PROGRAM, (
                    data["program_code"], 
                    data["program_name"], 
                    data["college_code"]
                ))
                new_program = cur.fetchone()
                conn.commit()
                return new_program

    def update(self, current_code, data):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(ProgramQueries.UPDATE_PROGRAM, (
                    data["program_code"], 
                    data["program_name"], 
                    data["college_code"],
                    current_code
                ))
                updated = cur.fetchone()
                conn.commit()
                return updated

    def delete(self, program_code):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(ProgramQueries.DELETE_PROGRAM, (program_code,))
                deleted = cur.fetchone()
                conn.commit()
                return deleted