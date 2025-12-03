from psycopg.rows import dict_row
from db import get_pool
from queries.program_queries import ProgramQueries

class ProgramRepository:
    def __init__(self):
        self.pool = get_pool()

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