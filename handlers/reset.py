"""Handler for /reset command."""
from aiogram import types
from aiogram.dispatcher import FSMContext

from create import dp, logger, i18n
from util.keyboards import create_menu_inline

_ = i18n.gettext


# @dp.message_handler(commands=['reset'], state='*')
async def command_reset(message: types.Message, state: FSMContext) -> None:
    """Reset the user allstate.

    :param message: Message object from user.
    :type message: Message
    :param state: FSM any state.
    :type state: FSMContext

    :return: None
    :rtype: None
    """
    await message.answer(_('Reset all state'), reply_markup=types.ReplyKeyboardRemove())
    if dp.current_state(user=message.from_user.id):
        await state.finish()
        await message.answer(_('The allstate reset'),
                             reply_markup=await create_menu_inline('main_menu', language=message.from_user.language_code))
        logger.info(
            f'Reset the allstate user {message.from_user.first_name} (id:{message.from_user.id})')
    else:
        await message.answer(_('The currency state not found'),
                             reply_markup=await create_menu_inline('main_menu', language=message.from_user.language_code))


def register_handlers_reset() -> None:
    """Register handlers for /reset command."""
    dp.register_message_handler(command_reset, commands=['reset'], state='*')


if __name__ == '__main__':
    pass
