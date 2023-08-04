"""Handler for /reset command"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from admin import checking
from admin.logsetting import logger
from util.keyboards import main_menu


# @dp.message_handler(commands=['reset'], state='*')
@checking.check_registration
async def command_reset(message: types.Message, state: FSMContext):
    """Check the user in the database and reset the allstate him."""
    await message.answer('Reset all state', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    await message.answer('The allstate reset', reply_markup=main_menu)
    logger.info(
        f'Reset the allstate user {message.from_user.first_name} (id:{message.from_user.id})')


def register_handlers_reset(dp: Dispatcher):
    dp.register_message_handler(command_reset, commands=['reset'], state='*')


if __name__ == '__main__':
    pass
