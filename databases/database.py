import asyncio
import asyncpg
from asyncpg import Record
import create
from typing import Any
from admin.logsetting import logger
import datetime

DB_NAME = create.DB_NAME
DB_USER = create.DB_USER
DB_PASSWORD = create.DB_PASSWORD
DB_HOST = create.DB_HOST
DB_PORT = create.DB_PORT


async def start_db() -> bool:
    """Create users and requests tables."""
    status: bool = False
    conn: Any | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                Id SERIAL PRIMARY KEY,
                UserId INTEGER UNIQUE,
                FirstName CHARACTER VARYING(30),
                FullName CHARACTER VARYING(30),
                DateRegistration TIMESTAMP DEFAULT NOW(),
                LanguageUser CHARACTER(2) DEFAULT 'ru'
            )
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                Id SERIAL PRIMARY KEY,
                UserId INTEGER REFERENCES users(UserId),
                TypeRequest CHARACTER VARYING(30),
                DateRequest TIMESTAMP DEFAULT NOW(),
                NumTokens INTEGER,
                Status BOOLEAN DEFAULT FALSE
            )
        """)
        status = True

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()
    return status


async def add_user_db(user_id: int,
                      first_name: str,
                      full_name: str, ) -> bool:
    """Add the new user to the users table."""
    status: bool = False
    conn: Any | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        async with conn.transaction():
            await conn.execute("""INSERT INTO users (UserId, FirstName, FullName, DateRegistration)
                                  VALUES ($1, $2, $3, $4)""",
                               user_id, first_name, full_name, datetime.datetime.now())
        status = True

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return status


async def add_request_db(user_id: int,
                         type_request: str,
                         num_tokens: int,
                         status_request: bool) -> bool:
    """Add the new request to the requests table."""
    status: bool = False
    conn: Any | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        async with conn.transaction():
            await conn.execute("""INSERT INTO requests (UserId, TypeRequest, DateRequest, NumTokens, Status)
                                  VALUES ($1, $2, $3, $4, $5)""",
                               user_id, type_request, datetime.datetime.now(), num_tokens, status_request)
        status = True

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return status


async def get_user_db(user_id: int) -> Record | None:
    """Get the data of user from the users' table by id."""
    _user: Record | None = None
    conn: Any | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        query = """SELECT * FROM users WHERE UserId=$1"""
        _user = await conn.fetchrow(query, user_id)

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return _user


async def get_user_lang_db(user_id: int) -> str | None:
    """Get the code of the user language from the users' table by id."""
    _user: dict[str, str] | None = None
    conn: Any | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        query = """SELECT languageuser FROM users WHERE UserId=$1"""
        _user = await conn.fetchrow(query, user_id)

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return _user['languageuser']


async def get_all_users_db() -> list[Record]:
    """Get all users from the users' table."""
    _users: list[Record] | None = None
    conn: Any | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        query = """ SELECT * FROM users """
        _users = await conn.fetch(query)

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return _users


async def get_requests_count_db() -> int:
    """Get the total number of requests from the requests' table."""
    _count: int | None = None
    conn: Any | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        query = """ SELECT COUNT(*) FROM requests """
        _count = await conn.fetchval(query)

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return _count


async def get_all_requests_db() -> list[Record]:
    """Get all user requests from the requests' table by user id."""
    _requests: list[Record] | None = None
    conn: Any | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        query = """ SELECT * FROM users JOIN requests ON users.UserId=requests.UserId """
        _requests = await conn.fetch(query)

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return _requests


if __name__ == '__main__':
    # print(asyncio.get_event_loop().run_until_complete(start_db()))
    # print(asyncio.get_event_loop().run_until_complete(add_user_db(777777777, 'Test', 'Test Test')))
    # print(asyncio.get_event_loop().run_until_complete(add_request_db(66666, 'Test', 100, True)))
    # print(asyncio.get_event_loop().run_until_complete(get_user_db(123456789)))
    print(asyncio.get_event_loop().run_until_complete(get_user_db(777777777)))
    # print(asyncio.get_event_loop().run_until_complete(get_all_users_db()))
    # print(asyncio.get_event_loop().run_until_complete(get_requests_count_db()))
    # print(asyncio.get_event_loop().run_until_complete(get_all_requests_db()))
    print(asyncio.get_event_loop().run_until_complete(get_user_db(777777777)).get('languageuser'))
