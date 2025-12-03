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