# !!!!! asyncpg
import psycopg2
from psycopg2.extensions import connection
import create
from admin.logsetting import logger
import datetime

DB_NAME = create.DB_NAME
DB_USER = create.DB_USER
DB_PASSWORD = create.DB_PASSWORD
DB_HOST = create.DB_HOST
DB_PORT = create.DB_PORT


def start_db() -> bool:
    """Create users and requests tables."""
    status: bool = False
    conn: connection | None = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    Id SERIAL PRIMARY KEY,
                    UserId INTEGER UNIQUE,
                    FirstName CHARACTER VARYING(30),
                    FullName CHARACTER VARYING(30),
                    DateRegistration TIMESTAMP DEFAULT NOW(),
                    LanguageUser CHARACTER(2) DEFAULT 'en'
                )""")
                cursor.execute("""CREATE TABLE IF NOT EXISTS requests (
                    Id SERIAL PRIMARY KEY,
                    UserId INTEGER REFERENCES users(UserId),
                    TypeRequest CHARACTER VARYING(30),
                    DateRequest TIMESTAMP DEFAULT NOW(),
                    NumTokens INTEGER,
                    Status BOOLEAN DEFAULT FALSE
                )""")
                conn.commit()
        status = True

    except psycopg2.DatabaseError as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            conn.close()
    return status


def add_user_db(user_id: int,
                first_name: str,
                full_name: str,) -> bool:
    """Add the new user to the users table."""
    status: bool = False
    conn: connection | None = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO users (UserId, FirstName, FullName, DateRegistration)
                                  VALUES (%s, %s, %s, %s)""",
                               (user_id, first_name, full_name, datetime.datetime.now()))
                conn.commit()
        status = True

    except psycopg2.DatabaseError as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            conn.close()
    return status


def add_request_db(user_id: int,
                   type_request: str,
                   num_tokens: int,
                   status_request: bool) -> bool:
    """Add the new request to the requests table."""
    status: bool = False
    conn: connection | None = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO requests (UserId, TypeRequest, DateRequest, NumTokens, Status)
                                  VALUES (%s, %s, %s, %s, %s)""",
                               (user_id, type_request, datetime.datetime.now(), num_tokens, status_request))
                conn.commit()
        status = True

    except psycopg2.DatabaseError as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            conn.close()
    return status


def get_user_db(user_id: int) -> tuple:
    """Get the user from the users' table by id."""
    conn: connection | None = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(" SELECT * FROM users WHERE UserId=%s ", (user_id,))
                return cursor.fetchone()

    except psycopg2.DatabaseError as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            conn.close()
    return ()


def get_all_users_db() -> list:
    """Get all users from the users' table."""
    conn: connection | None = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(" SELECT * FROM users ")
                return cursor.fetchall()

    except psycopg2.DatabaseError as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            conn.close()
    return []


def get_requests_count_db() -> int:
    """Get the total number of requests from the requests' table."""
    conn: connection | None = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(" SELECT COUNT(*) FROM requests ")
                return cursor.fetchone()[0]

    except psycopg2.DatabaseError as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            conn.close()
    return 0


if __name__ == '__main__':
    pass
