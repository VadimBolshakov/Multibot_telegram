"""Authentication new user by password, used FSM."""

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from create import bot, PASSWORD, ADMIN_ID, db, logger, i18n
from util.keyboards import create_menu_inline

_ = i18n.gettext


class RegisterFSM(StatesGroup):
    """Class for register FSM.

    Args:
        StatesGroup (StatesGroup):Basis class for register FSM.

    Attributes:
        password (State): State for input password.
    """

    password = State()


# @dp.message_handler(commands=['start'], state=None)
async def command_start(message: types.Message) -> None:
    """Check user in database and send message with password or welcome message.

    :param message: Message object from user.
    :type message: Message

    :return: None
    :rtype: None
    """
    logger.info(
        f'Entry to start handler user {message.from_user.first_name} (id:{message.from_user.id})')
    if await db.get_user_db(message.from_user.id) is None:
        await message.answer(_('Enter password'))
        """Set FSM state to password."""
        await RegisterFSM.password.set()
    else:
        await message.answer(_('Hello {full_name}.\n'
                               'You already have registered.\n'
                               'Welcome to my bot \U0001F604').format(full_name=message.from_user.full_name),
                             reply_markup=await create_menu_inline('main_menu', language=message.from_user.language_code))
        logger.info(
            f'Exit from start handler user {message.from_user.first_name} (id:{message.from_user.id})')


# @dp.message_handler(state=RegisterFSM.password)
async def input_password(message: types.Message, state: FSMContext) -> None:
    """Check password and add user to database.

    :param message: Message object from user.
    :type message: Message
    :param state: FSM state.
    :type state: FSMContext

    :return: None
    :rtype: None
    """
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
        await bot.send_message(message.chat.id, _('Hello {full_name}.\n'
                                                  'You are registered successfully.\n'
                                                  'This is a multi-function bot.\n'
                                                  'Enter command /help to learn more.\n'
                                                  'Welcome to my bot\U0001F604').format(full_name=message.from_user.full_name),
                               reply_markup=await create_menu_inline('main_menu', language=message.from_user.language_code))
        await state.finish()
    else:
        logger.warning(
            f'Enter password is incorrect user {message.from_user.first_name} (id:{message.from_user.id})')
        await message.answer(_('The password is incorrect'))
        await state.finish()


def register_handlers_start(dp: Dispatcher) -> None:
    """Register handlers for /start command.

    :param dp: Dispatcher object
    :type dp: Dispatcher

    :return: None
    :rtype: None
    """
    dp.register_message_handler(command_start, commands=['start'], state=None)
    dp.register_message_handler(input_password, state=RegisterFSM.password)


if __name__ == '__main__':
    pass
