from aiogram import types
from admin.logsetting import logger
from databases import database
from create import ADMIN_ID


def check_registration(fn):
    """Checking the registration user"""
    async def wrapper(message: types.Message):
        user_first_name = message.from_user.first_name
        user_id = message.from_user.id
        if await database.get_user_db(message.from_user.id) is None:
            await message.answer("Вы не зарегистрированы. Введите команду /start")
            # await message.answer(f"You are not registered. Enter the command /start")
            logger.warning(f'Fail the registration check user {user_first_name} (id:{user_id})')
            return
        
        logger.info(f'Passed the registration check user {user_first_name} (id:{user_id})')

        return await fn(message)
    return wrapper


def check_admin(fn):
    """Checking the admin user"""
    async def wrapper(message: types.Message):
        user_first_name = message.from_user.first_name
        user_id = message.from_user.id
        try:
            if await database.get_user_db(message.from_user.id) is None:
                await message.answer('Вы не зарегистрированы. Введите команду /start')
                logger.warning(f'Fail the registration check user {user_first_name} (id:{user_id})')
                return

            if not await database.get_user_admin_db(message.from_user.id):
                await message.answer('У вас нет доступа к этой команде')
                # await message.answer('permission denied')
                logger.warning(f'Fail the admin check user {user_first_name} (id:{user_id})')
                return
            logger.info(f'Passed the admin check user {user_first_name} (id:{user_id})')

        except Exception as e:
            logger.exception(f'Error DB reads: {str(e)} from {user_first_name} (id:{user_id}')
            await message.answer(f'Error DB reads: {str(e)} from {user_first_name} (id:{user_id}')
            return
        return await fn(message)
    return wrapper
