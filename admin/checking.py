"""Checking the user's registration and admin rights"""
from logging import Logger

from aiogram import types

from databases.database import DataBaseMain


def check_registration(logger: Logger, database: DataBaseMain):
    """Decorator checking the registration user

    :param logger: logging
    :type logger: Logger
    :param database: Database
    :type database: DataBaseMain

    :return: Decorator
    :rtype: function
    """
    def decorator(fn):
        async def wrapper(message: types.Message):
            user_first_name = message.from_user.first_name
            user_id = message.from_user.id
            if await database.get_user_db(user_id) is None:
                await message.answer('You are not registered. Enter the command /start')
                logger.warning(f'Fail the registration check user {user_first_name} (id:{user_id})')
                return

            logger.info(f'Passed the registration check user {user_first_name} (id:{user_id})')

            return await fn(message)
        return wrapper
    return decorator


def check_admin(logger: Logger, database: DataBaseMain):
    """Decorator checking the admin rights user

    :param logger: logging
    :type logger: Logger
    :param database: Database
    :type database: DataBaseMain

    :return: Decorator
    :rtype: function
    """
    def decorator(fn):
        async def wrapper(message: types.Message):
            user_first_name = message.from_user.first_name
            user_id = message.from_user.id
            try:
                if await database.get_user_db(message.from_user.id) is None:
                    await message.answer('You are not registered. Enter the command /start')
                    logger.warning(f'Fail the registration check user {user_first_name} (id:{user_id})')
                    return

                if not await database.get_user_status_admin_db(message.from_user.id):
                    await message.answer('permission denied')
                    logger.warning(f'Fail the admin check user {user_first_name} (id:{user_id})')
                    return
                logger.info(f'Passed the admin check user {user_first_name} (id:{user_id})')

            except Exception as e:
                logger.exception(f'Error DB reads: {str(e)} from {user_first_name} (id:{user_id}')
                await message.answer(f'Error DB reads: {str(e)} from {user_first_name} (id:{user_id}')
                return
            return await fn(message)
        return wrapper
    return decorator
