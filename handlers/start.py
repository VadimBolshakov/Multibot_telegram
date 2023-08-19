"""Authentication new user by password, used FSM."""

from aiogram import Dispatcher, types
from create import bot, PASSWORD, ADMIN_ID, db, logger
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from util.keyboards import main_menu


class RegisterFSM(StatesGroup):
    password = State()


# @dp.message_handler(commands=['start'], state=None)
async def command_start(message: types.Message):
    """Check user in database and send message with password or welcome message."""
    logger.info(
        f'Entry to start handler user {message.from_user.first_name} (id:{message.from_user.id})')
    if await db.get_user_db(message.from_user.id) is None:
        await message.answer('Enter password')
        """Set FSM state to password."""
        await RegisterFSM.password.set()
    else:
        await message.answer(f'Hello {message.from_user.full_name}.\n'
                             f'You already have registered.\n'
                             f'Welcome to my bot \U0001F604', reply_markup=main_menu)
        logger.info(
            f'Exit from start handler user {message.from_user.first_name} (id:{message.from_user.id})')


# @dp.message_handler(state=RegisterFSM.password)
async def input_password(message: types.Message, state: FSMContext):
    """Check password and add user to database."""
    async with state.proxy() as data:
        data['password'] = message.text.split()
    if data['password'][0] == PASSWORD:
        status_admin: bool = True if message.from_user.id == int(ADMIN_ID) else False
        await db.add_user_db(user_id=message.from_user.id,
                             first_name=message.from_user.first_name,
                             full_name=message.from_user.full_name,
                             lang=message.from_user.language_code,
                             status_admin=status_admin)
        logger.info(
            f'New user registrate success {message.from_user.first_name} (id:{message.from_user.id})')
        await bot.send_message(message.chat.id, f'Hello {message.from_user.full_name}.\n'
                                                f'You are registered successfully.\n'
                                                f'This is a multi-function bot.\n'
                                                f'Enter command /help to learn more.\n'
                                                f'Welcome to my bot\U0001F604', reply_markup=main_menu)
        await state.finish()
    else:
        logger.warning(
            f'Enter password is incorrect user {message.from_user.first_name} (id:{message.from_user.id})')
        await message.answer('The password is incorrect')
        await message.answer('Enter password')
        await state.finish()


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state=None)
    dp.register_message_handler(input_password, state=RegisterFSM.password)


if __name__ == '__main__':
    pass
