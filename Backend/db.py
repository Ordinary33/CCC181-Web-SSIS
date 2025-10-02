import os
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")


pool = ConnectionPool(conninfo=DATABASE_URL)


def get_pool():
    return pool