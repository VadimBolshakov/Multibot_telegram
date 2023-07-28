import asyncio
import asyncpg
from asyncpg import Record, Connection
import create
from admin.logsetting import logger
import datetime

DB_NAME = create.DB_NAME
DB_USER = create.DB_USER
DB_PASSWORD = create.DB_PASSWORD
DB_HOST = create.DB_HOST
DB_PORT = create.DB_PORT


async def start_db() -> bool:
    """Create users and requests tables. Return True if tables created, else False."""
    status: bool = False
    conn: Connection | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                Id SERIAL PRIMARY KEY,
                UserId INTEGER UNIQUE,
                FirstName CHARACTER VARYING(30),
                FullName CHARACTER VARYING(30),
                DateRegistration TIMESTAMP DEFAULT NOW(),
                LanguageUser CHARACTER(2) DEFAULT 'en',
                StatusAdmin BOOLEAN DEFAULT FALSE,
                Is_banned BOOLEAN DEFAULT FALSE,
                DateBanned TIMESTAMP DEFAULT NULL
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
                      full_name: str,
                      status_admin: bool = False) -> bool:
    """Add the new user to the users table. Return True if user added, else False."""
    status: bool = False
    conn: Connection | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        async with conn.transaction():
            await conn.execute("""INSERT INTO users (UserId, FirstName, FullName, DateRegistration, StatusAdmin)
                                  VALUES ($1, $2, $3, $4, $5)""",
                               user_id, first_name, full_name, datetime.datetime.now(), status_admin)
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
    """Add the new request to the requests table. Return True if request added, else False."""
    status: bool = False
    conn: Connection | None = None
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
    conn: Connection | None = None
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
    conn: Connection | None = None
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


async def get_user_admin_db(user_id: int) -> bool | None:
    """Get the status of the user admin from the users' table by id. Return True if user admin, else False."""
    _user: dict[str, bool] | None = None
    conn: Connection | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        query = """SELECT statusadmin FROM users WHERE UserId=$1"""
        _user = await conn.fetchrow(query, user_id)

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return _user['statusadmin']


async def get_user_banned_db(user_id: int) -> bool | None:
    """Get the status of the user banned from the users' table by id. Return True if user banned, else False."""
    _user: dict[str, bool] | None = None
    conn: Connection | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        query = """SELECT is_banned FROM users WHERE UserId=$1"""
        _user = await conn.fetchrow(query, user_id)

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return _user['is_banned']


async def get_all_users_db() -> list[Record]:
    """Get all users from the users' table."""
    _users: list[Record] | None = None
    conn: Connection | None = None
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
    conn: Connection | None = None
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
    conn: Connection | None = None
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


async def up_user_admin_db(user_id: int) -> bool:
    """Update the user status to admin in the users' table by id. Return True if the status is updated, False otherwise."""
    status: bool = False
    conn: Connection | None = None
    _status_admin: bool | None = await get_user_admin_db(user_id)

    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        async with conn.transaction():
            await conn.execute("""UPDATE users SET StatusAdmin=$1 WHERE UserId=$2""",
                               not _status_admin, user_id)
        status = True

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return status


async def up_user_lang_db(user_id: int, lang: str) -> bool:
    """Update the user language in the users' table by id. Return True if the language is updated, False otherwise."""
    status: bool = False
    conn: Connection | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        async with conn.transaction():
            await conn.execute("""UPDATE users SET LanguageUser=$1 WHERE UserId=$2""",
                               lang, user_id)
        status = True

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return status


async def up_user_banned_db(user_id: int) -> bool:
    """Update the user status to banned in the users' table by id. Return True if the user is banned, False otherwise."""
    status: bool = False
    conn: Connection | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        async with conn.transaction():
            await conn.execute("""UPDATE users SET Is_banned=$1, DateBanned=$2 WHERE UserId=$3""",
                               True, datetime.datetime.now(), user_id)
        status = True

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return status


async def del_user_db(user_id: int) -> bool:
    """Delete the user from the users' table by id. Return True if the user is deleted, False otherwise."""
    status: bool = False
    conn: Connection | None = None
    try:
        conn = await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        async with conn.transaction():
            await conn.execute("""DELETE FROM users WHERE UserId=$1""",
                               user_id)
        status = True

    except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
        logger.exception(f'DatabaseError: {str(e)}')

    finally:
        if conn is not None:
            await conn.close()

    return status


if __name__ == '__main__':
    print(asyncio.get_event_loop().run_until_complete(start_db()))
    # print(asyncio.get_event_loop().run_until_complete(del_user_db(22222)))
    # print(asyncio.get_event_loop().run_until_complete(del_user_db(11111)))
    # print(asyncio.get_event_loop().run_until_complete(del_user_db(33333)))
    print(asyncio.get_event_loop().run_until_complete(add_user_db(1661414346, 'Vadim', 'Vadim')))
    print(asyncio.get_event_loop().run_until_complete(add_user_db(11111, 'Test1', 'Test Test1')))
    print(asyncio.get_event_loop().run_until_complete(add_user_db(22222, 'Test2', 'Test Test2')))
    print(asyncio.get_event_loop().run_until_complete(add_user_db(33333, 'Test3', 'Test Test3')))
    print(asyncio.get_event_loop().run_until_complete(add_request_db(11111, 'Test', 100, True)))
    print(asyncio.get_event_loop().run_until_complete(get_user_db(11111)))
    print(asyncio.get_event_loop().run_until_complete(get_user_db(22222)))
    print(asyncio.get_event_loop().run_until_complete(get_all_users_db()))
    print(asyncio.get_event_loop().run_until_complete(get_requests_count_db()))
    print(asyncio.get_event_loop().run_until_complete(get_all_requests_db()))
    print(asyncio.get_event_loop().run_until_complete(get_user_lang_db(11111)))
    print(asyncio.get_event_loop().run_until_complete(up_user_admin_db(11111)))
    print(asyncio.get_event_loop().run_until_complete(up_user_lang_db(11111, 'ru')))
    print(asyncio.get_event_loop().run_until_complete(up_user_banned_db(11111)))
    print(asyncio.get_event_loop().run_until_complete(get_user_db(11111)))
    print(asyncio.get_event_loop().run_until_complete(get_user_admin_db(11111)))
    print(asyncio.get_event_loop().run_until_complete(get_user_lang_db(11111)))
    print(asyncio.get_event_loop().run_until_complete(get_user_banned_db(11111)))
    print(asyncio.get_event_loop().run_until_complete(up_user_admin_db(11111)))
    print(asyncio.get_event_loop().run_until_complete(get_user_admin_db(11111)))
