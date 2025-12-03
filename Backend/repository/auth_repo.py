from db import get_pool
from queries.auth_queries import AuthQueries  

class UserRepository:
    def __init__(self):
        self.pool = get_pool()

    def get_by_username(self, username):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(AuthQueries.GET_USER_BY_USERNAME, (username,))
                return cur.fetchone()

    def create(self, username, password_hash):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    AuthQueries.INSERT_USER, 
                    (username, password_hash)
                )
                user_id = cur.fetchone()[0]
                conn.commit() 
                return user_id