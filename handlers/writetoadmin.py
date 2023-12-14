"""This module contains handler for command /toadmin."""
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create import dp, db, logger, i18n, bot, ADMIN_ID
from util.keyboards import create_menu_inline

_ = i18n.gettext


class WritetoadminFSM(StatesGroup):
    """Class for change language FSM.

    Args:
        StatesGroup (StatesGroup):Basis class for change language FSM.

    Attributes:
        write_messages (State): State for change language.
    """

    write_messages = State()


# @dp.message_handler(commands=['toadmin'], state=None)
async def command_toadmin(message: types.Message) -> None:
    """Write to admin.

    :param message: Message object from user
    :type message: Message

    :return: None
    """

    logger.info(
        f'Entry to writetoadmin handler user {message.from_user.first_name} (id:{message.from_user.id})')

    await message.answer(_('Please. Write your message'), reply_markup=types.ReplyKeyboardRemove())

    await WritetoadminFSM.write_messages.set()


@dp.message_handler(state=WritetoadminFSM.write_messages)
async def write_messages(message: types.Message, state: FSMContext) -> None:
    """Write to admin.

    :param message: Message object from user
    :type message: Message
    :param state: State object
    :type state: State

    :return: None
    """
    await message.answer(_('Please, wait'))
    async with state.proxy() as data:
        data['message'] = message.text
    await message.answer(_('Your message: {message}').format(message=data['message']))
    await message.answer(_('Your message sent to admin'))
    await bot.send_message(chat_id=ADMIN_ID, text=data['message'] +
                                                                    '\n' + message.from_user.first_name + '\n' + str(message.from_user.id))
    await state.finish()
    logger.info(
        f'Exit from writetoadmin handler user {message.from_user.first_name} (id:{message.from_user.id})')
    await message.answer(_('Welcome to Main menu'),
                         reply_markup=await create_menu_inline('main_menu',
                                                               language=await db.get_user_lang_db(message.from_user.id)))


def register_handlers_toadmin() -> None:
    """Register handlers for toadmin.

    :return: None
    :rtype: None
    """
    dp.register_message_handler(command_toadmin, commands=['toadmin'])
    dp.register_message_handler(write_messages, state=WritetoadminFSM.write_messages)


if __name__ == '__main__':
    pass
