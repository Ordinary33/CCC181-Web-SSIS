from psycopg.rows import dict_row
from db import get_pool
from queries.college_queries import CollegeQueries

class CollegeRepository:
    def __init__(self):
        self.pool = get_pool()

    def get_all(self):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(CollegeQueries.SELECT_ALL)
                return cur.fetchall()

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