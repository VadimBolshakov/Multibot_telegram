"""Admin handler."""
import asyncio

from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from asyncpg import Record

from admin import checking
from admin.logsetting import logger
from create import bot
from databases import database
from models.admin import AdminResponse


class AdminFSM(StatesGroup):
    broadcast = State()
    baninguser = State()
    statusadmin = State()


# @dp.message_handler(commands=['admin'])
@checking.check_admin
async def admin(message: types.Message):
    """Send message to admin about using commands."""
    await message.answer('Admin panel suggest using next commands:\n'
                         '/getlog - send log file to telegram\n'
                         '/getemail - send log file to email\n'
                         '/getusers - send id and users of this chat to admin\n'
                         '/getrequests - send number of requests to admin\n'
                         '/sendall - send message to all users\n'
                         '/banneruser - ban user\n'
                         '/statusadmin - change status admin user\n')


# @dp.message_handler(commands=['getlog'])
@checking.check_admin
async def send_log(message: types.Message):
    """Send log file to admin in telegram."""
    await AdminResponse(message).send_log()


# @dp.message_handler(commands=['getemail'])
@checking.check_admin
async def send_email_lod(message: types.Message):
    """Send log file to admin in email."""
    await AdminResponse(message).send_email_lod()


# @dp.message_handler(commands=['getusers'])
@checking.check_admin
async def send_users(message: types.Message):
    """Send id and users of this chat to admin."""
    await AdminResponse(message).send_users()


# @dp.message_handler(commands=['getrequests'])
@checking.check_admin
async def send_requests(message: types.Message):
    """Send number of requests to admin."""
    await AdminResponse(message).send_requests()


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
    users: list[Record] = await database.get_all_users_db()
    if not users:
        await message.answer('Users not found')
        await state.finish()
        return
    count = 0
    for user in users:
        try:
            if await bot.send_message(user.get('userid'), data['broadcast']):
                count += 1
                await asyncio.sleep(0.05)
        except Exception as e:
            logger.exception(f'Error send message to {user} {e}')
            await message.answer(f'Error send message to {user} {e}')
    await message.answer('It is done. It was sent ' + str(count) + ' messages')
    await state.finish()


# @dp.message_handler(commands=['banneruser'], state=None)
@checking.check_admin
async def baning_user_id(message: types.Message):
    """Get id baning user."""
    await message.answer('Enter baning user id (enter "/cancel" to cancel)')
    await AdminFSM.baninguser.set()


# @dp.message_handler(state=AdminFSM.baninguser)
async def ban_user(message: types.Message, state: FSMContext):
    """Ban user by id."""
    async with state.proxy() as data:
        data['baning_user'] = message.text

    if data['baning_user'] == '/cancel':
        await message.answer('Cancel')
        await state.finish()
        return

    try:
        user_id = int(data['baning_user'])
    except ValueError:
        await message.answer('Error id')
        await state.finish()
        return

    if not await database.get_user_db(user_id):
        await message.answer('User not found')
        await state.finish()
        return

    if await database.up_user_banned_db(user_id):
        await message.answer(f'Banned user {user_id} is {await database.get_user_banned_db(user_id)}. ')
    else:
        await message.answer(f'Error ban user {user_id}')

    await state.finish()


# @dp.message_handler(commands=['statusadmin'], state=None)
@checking.check_admin
async def status_admin_id(message: types.Message):
    """Get status admin."""
    await message.answer('Enter status admin user id (enter "/cancel" to cancel)')
    await AdminFSM.statusadmin.set()


# @dp.message_handler(state=AdminFSM.statusadmin)
async def status_admin(message: types.Message, state: FSMContext):
    """Change status admin."""
    async with state.proxy() as data:
        data['status_admin'] = message.text

    if data['status_admin'] == '/cancel':
        await message.answer('Cancel')
        await state.finish()
        return

    try:
        user_id = int(data['status_admin'])
    except ValueError:
        await message.answer('Error id')
        await state.finish()
        return

    if not await database.get_user_db(user_id):
        await message.answer('User not found')
        await state.finish()
        return

    if await database.up_user_admin_db(user_id):
        await message.answer(f'User {user_id} status admin changed.\n'
                             f'Now status admin user {user_id} is {await database.get_user_admin_db(user_id)}.')
    else:
        await message.answer(f'Error user {user_id} change status admin')

    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin, commands=['admin'])
    dp.register_message_handler(send_log, commands=['getlog'])
    dp.register_message_handler(send_email_lod, commands=['getemail'])
    dp.register_message_handler(send_users, commands=['getusers'])
    dp.register_message_handler(send_requests, commands=['getrequests'])
    dp.register_message_handler(send_all, commands=['sendall'], state=None)
    dp.register_message_handler(send_all_message, state=AdminFSM.broadcast)
    dp.register_message_handler(baning_user_id, commands=['banneruser'], state=None)
    dp.register_message_handler(ban_user, state=AdminFSM.baninguser)
    dp.register_message_handler(status_admin_id, commands=['statusadmin'], state=None)
    dp.register_message_handler(status_admin, state=AdminFSM.statusadmin)


if __name__ == '__main__':
    pass
