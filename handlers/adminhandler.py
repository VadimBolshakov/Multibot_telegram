import asyncio

from create import bot
from admin.logsetting import logger
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from admin import smtp
from databases import database
from datetime import datetime
from create import LOG_FILE
from admin import checking
from asyncpg import Record


class AdminFSM(StatesGroup):
    broadcast = State()


# @dp.message_handler(user_id=ADMIN_ID, commands=['admin'])
@checking.check_admin
async def admin(message: types.Message):
    """Send message to admin about using commands."""
    await message.answer('Admin panel suggest using next commands:\n'
                         '/getlog - send log file to telegram\n'
                         '/getemail - send log file to email\n'
                         '/getusers - send id and users of this chat to admin\n'
                         '/getrequests - send number of requests to admin\n'
                         '/sendall - send message to all users\n')


# @dp.message_handler(commands=['getlog'])
@checking.check_admin
async def send_log(message: types.Message):
    """Send log file to admin in telegram."""
    try:
        with open(LOG_FILE, 'rb') as file:
            await message.answer_document(file)
    except FileNotFoundError as e:
        logger.exception(f'Error: {str(e)}')
        await message.answer('Log file not found')
    except Exception as e:
        logger.exception(f'Error: {str(e)}')
        await message.answer('Error send log file')


# @dp.message_handler(commands=['getemail'])
@checking.check_admin
async def send_email_lod(message: types.Message):
    """Send log file to admin in email."""
    subject = f'Log file by {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    if smtp.send_email(subject=subject, file=LOG_FILE, attach_file=True):
        await message.answer('Log file send to email')
    else:
        await message.answer('Error send log file to email')


# @dp.message_handler(commands=['getusers'])
@checking.check_admin
async def send_users(message: types.Message):
    """Send id and users of this chat to admin."""
    users: list[Record] = asyncio.get_event_loop().run_until_complete(database.get_all_users_db())
    if not users:
        await message.answer('Users not found')
        return
    for user in users:
        await message.answer(user.get('userid') + ' ' + user.get('firstname'))


# @dp.message_handler(commands=['getrequests'])
@checking.check_admin
async def send_requests(message: types.Message):
    """Send number of requests to admin."""
    requests = asyncio.get_event_loop().run_until_complete(database.get_requests_count_db())
    await message.answer(f'Number of  requests is {requests}')


# @dp.message_handler(commands=['sendall'], state=None)
@checking.check_admin
async def send_all(message: types.Message):
    """Send message to all users."""
    await message.answer('Enter message (enter "/cancel" to cancel)')
    await AdminFSM.broadcast.set()


# @dp.message_handler(state=AdminFSM.broadcast)
async def send_all_message(message: types.Message, state: FSMContext):
    """Send message to all users."""
    async with state.proxy() as data:
        data['broadcast'] = message.text
    if data['broadcast'] == '/cancel':
        await message.answer('Cancel')
        await state.finish()
        return
    users: list[Record] = asyncio.get_event_loop().run_until_complete(database.get_all_users_db())
    if not users:
        await message.answer('Users not found')
        await state.finish()
        return
    for user in users:
        try:
            await bot.send_message(user.get('userid'), data['broadcast'])
        except Exception as e:
            logger.exception(f'Error send message to {user} {e}')
            await message.answer(f'Error send message to {user} {e}')
    await message.answer('Message send')
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin, commands=['admin'])
    dp.register_message_handler(send_log, commands=['getlog'])
    dp.register_message_handler(send_email_lod, commands=['getemail'])
    dp.register_message_handler(send_users, commands=['getusers'])
    dp.register_message_handler(send_requests, commands=['getrequests'])
    dp.register_message_handler(send_all, commands=['sendall'], state=None)
    dp.register_message_handler(send_all_message, state=AdminFSM.broadcast)


if __name__ == '__main__':
    pass
