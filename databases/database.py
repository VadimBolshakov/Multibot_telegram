"""This module provides the interaction with the database."""
import datetime
from logging import Logger
from typing import Optional

import asyncpg
from asyncpg import Record, Connection


class DataBaseMain:
    """Class project database

    :param db_user: Database user
    :type db_user: str
    :param db_password: Database password
    :type db_password: str
    :param db_host: Database host
    :type db_host: str
    :param db_port: Database port
    :type db_port: str
    :param db_name: Database name
    :type db_name: str
    :param logger: logging as class Logger if existed, defaults to None
    :type logger:

    :return: None
    """

    def __init__(self, db_user: str, db_password: str, db_host: str, db_port: str, db_name: str, logger: Optional[Logger] = None) -> None:
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.logger: Logger = logger
        # Create a pool of connections to the database
        self.conn: Optional[Connection] = None
        # Data source name
        self.dsn: str = f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'

    async def close(self) -> None:
        """Close the connection to the database."""
        if self.conn is not None:
            await self.conn.close()

    async def start_db(self) -> bool:
        """Create users and requests tables. Return True if tables created, else False."""
        _status: bool = False
        try:
            self.conn = await asyncpg.connect(self.dsn)
            await self.conn.execute("""
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

            await self.conn.execute("""
                CREATE TABLE IF NOT EXISTS requests (
                    Id SERIAL PRIMARY KEY,
                    UserId INTEGER REFERENCES users(UserId),
                    TypeRequest CHARACTER VARYING(30),
                    DateRequest TIMESTAMP DEFAULT NOW(),
                    NumTokens INTEGER,
                    Status BOOLEAN DEFAULT FALSE
                )
            """)
            _status = True

        except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
            if self.logger is not None:
                self.logger.exception(f'DatabaseError: {str(e)}')

        finally:
            if self.conn is not None:
                await self.conn.close()
        return _status

    async def add_user_db(self,
                          user_id: int,
                          first_name: str,
                          full_name: str,
                          dt: datetime.datetime = datetime.datetime.now(),
                          lang: str = 'en',
                          status_admin: bool = False) -> bool:
        """Add the new user to the users table. Return True if user added, else False."""
        _status: bool = False
        try:
            self.conn = await asyncpg.connect(self.dsn)

            async with self.conn.transaction():
                await self.conn.execute("""INSERT INTO users (UserId, FirstName, FullName, DateRegistration, LanguageUser, StatusAdmin)
                                      VALUES ($1, $2, $3, $4, $5, $6)""",
                                        user_id, first_name, full_name, dt, lang, status_admin)
            _status = True

        except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
            if self.logger is not None:
                self.logger.exception(f'DatabaseError: {str(e)}')

        finally:
            if self.conn is not None:
                await self.conn.close()

        return _status

    async def add_request_db(self,
                             user_id: int,
                             type_request: str,
                             num_tokens: int,
                             status_request: bool,
                             dt: datetime.datetime = datetime.datetime.now()) -> bool:
        """Add the new request to the requests table. Return True if request added, else False."""
        _status: bool = False
        try:
            self.conn = await asyncpg.connect(self.dsn)

            async with self.conn.transaction():
                await self.conn.execute("""INSERT INTO requests (UserId, TypeRequest, DateRequest, NumTokens, Status)
                                      VALUES ($1, $2, $3, $4, $5)""",
                                        user_id, type_request, dt, num_tokens, status_request)
            _status = True

        except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
            if self.logger is not None:
                self.logger.exception(f'DatabaseError: {str(e)}')

        finally:
            if self.conn is not None:
                await self.conn.close()

        return _status

    async def get_user_db(self, user_id: int) -> Optional[Record]:
        """Get the data of user from the users' table by id. Return None if user not found."""
        _user: Optional[Record] = None
        try:
            self.conn = await asyncpg.connect(self.dsn)
            _query = """SELECT * FROM users WHERE UserId=$1"""
            _user = await self.conn.fetchrow(_query, user_id)

        except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
            if self.logger is not None:
                self.logger.exception(f'DatabaseError: {str(e)}')

        finally:
            if self.conn is not None:
                await self.conn.close()

        return _user

    async def get_all_users_db(self) -> list[Record]:
        """Get all users from the users' table."""
        _users: list[Record] | None = None
        try:
            self.conn = await asyncpg.connect(self.dsn)
            _query = """ SELECT * FROM users """
            _users = await self.conn.fetch(_query)

        except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
            if self.logger is not None:
                self.logger.exception(f'DatabaseError: {str(e)}')

        finally:
            if self.conn is not None:
                await self.conn.close()

        return _users

    async def get_requests_count_db(self) -> int:
        """Get the total number of requests from the requests' table."""
        _count: int | None = None
        try:
            self.conn = await asyncpg.connect(self.dsn)
            _query = """ SELECT COUNT(*) FROM requests """
            _count = await self.conn.fetchval(_query)

        except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
            if self.logger is not None:
                self.logger.exception(f'DatabaseError: {str(e)}')

        finally:
            if self.conn is not None:
                await self.conn.close()

        return _count

    async def get_all_requests_db(self) -> list[Record]:
        """Get all user requests from the requests' table by user id."""
        _requests: list[Record] | None = None
        try:
            self.conn = await asyncpg.connect(self.dsn)
            _query = """ SELECT * FROM users JOIN requests ON users.UserId=requests.UserId """
            _requests = await self.conn.fetch(_query)

        except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
            if self.logger is not None:
                self.logger.exception(f'DatabaseError: {str(e)}')

        finally:
            if self.conn is not None:
                await self.conn.close()

        return _requests

    async def get_user_lang_db(self, user_id: int) -> str:
        """Get the user language from the users' table by id. Return 'en' if user not found."""
        _lang: str = 'en'
        _user: Record | None = await self.get_user_db(user_id)

        if _user is None:
            return _lang

        _lang = _user.get('languageuser')
        return _lang

    async def get_user_status_admin_db(self, user_id: int) -> bool:
        """Get the user status from the users' table by id. Return False if user not found."""
        _status: bool = False
        _user: Record | None = await self.get_user_db(user_id)

        if _user is None:
            return _status

        _status = _user.get('statusadmin')
        return _status

    async def get_user_banned_db(self, user_id: int) -> bool:
        """Get the user status from the users' table by id. Return False if user not found."""
        _status: bool = False
        _user: Record | None = await self.get_user_db(user_id)

        if _user is None:
            return _status

        _status = _user.get('is_banned')
        return _status

    async def up_user_admin_db(self, user_id: int) -> bool:
        """Change the user status to admin in the users' table by id. Return True if the status was changed, False otherwise."""
        _status: bool = False
        _user: Record | None = await self.get_user_db(user_id)

        if _user is None:
            return _status

        try:
            self.conn = await asyncpg.connect(self.dsn)

            async with self.conn.transaction():
                await self.conn.execute("""UPDATE users SET StatusAdmin=$1 WHERE UserId=$2""",
                                        not _user.get('StatusAdmin'), user_id)
            _status = True

        except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
            if self.logger is not None:
                self.logger.exception(f'DatabaseError: {str(e)}')

        finally:
            if self.conn is not None:
                await self.conn.close()

        return _status

    async def up_user_lang_db(self, user_id: int, lang: str) -> bool:
        """Update the user language in the users' table by id. Return True if the language is updated, False otherwise."""
        _status: bool = False

        if await self.get_user_db(user_id) is None:
            return _status

        try:
            self.conn = await asyncpg.connect(self.dsn)

            async with self.conn.transaction():
                await self.conn.execute("""UPDATE users SET LanguageUser=$1 WHERE UserId=$2""",
                                        lang, user_id)
            _status = True

        except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
            if self.logger is not None:
                self.logger.exception(f'DatabaseError: {str(e)}')

        finally:
            if self.conn is not None:
                await self.conn.close()

        return _status

    async def up_user_banned_db(self, user_id: int, dt: datetime = datetime.datetime.now()) -> bool:
        """Update the user status to banned in the users' table by id. Return True if the user is banned, False otherwise."""
        _status: bool = False

        if await self.get_user_db(user_id) is None:
            return _status

        try:
            self.conn = await asyncpg.connect(self.dsn)

            async with self.conn.transaction():
                await self.conn.execute("""UPDATE users SET Is_banned=$1, DateBanned=$2 WHERE UserId=$3""",
                                        True, dt, user_id)
            _status = True

        except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
            if self.logger is not None:
                self.logger.exception(f'DatabaseError: {str(e)}')

        finally:
            if self.conn is not None:
                await self.conn.close()

        return _status

    async def del_user_db(self, user_id: int) -> bool:
        """Delete the user from the users' table by id. Return True if the user is deleted, False otherwise."""
        _status: bool = False
        try:
            self.conn = await asyncpg.connect(self.dsn)

            async with self.conn.transaction():
                await self.conn.execute("""DELETE FROM users WHERE UserId=$1""",
                                        user_id)
            _status = True

        except (asyncpg.PostgresConnectionError, asyncpg.DataError, asyncpg.PostgresError) as e:
            if self.logger is not None:
                self.logger.exception(f'DatabaseError: {str(e)}')

        finally:
            if self.conn is not None:
                await self.conn.close()

        return _status


if __name__ == '__main__':
    pass
