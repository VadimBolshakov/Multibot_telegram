"""Handler for /reset command"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from create import dp, logger, i18n
from util.keyboards import main_menu

_ = i18n.gettext


# @dp.message_handler(commands=['reset'], state='*')
async def command_reset(message: types.Message, state: FSMContext):
    """Check the user in the database and reset the allstate him."""
    await message.answer(_('Reset all state'), reply_markup=types.ReplyKeyboardRemove())
    if dp.current_state(user=message.from_user.id):
        await state.finish()
        await message.answer(_('The allstate reset'), reply_markup=main_menu)
        logger.info(
            f'Reset the allstate user {message.from_user.first_name} (id:{message.from_user.id})')
    else:
        await message.answer(_('The currency state not found'), reply_markup=main_menu)


def register_handlers_reset(dp: Dispatcher):
    dp.register_message_handler(command_reset, commands=['reset'], state='*')


if __name__ == '__main__':
    pass
