from aiogram import Dispatcher, types
from admin import checking
from admin.logsetting import logger
from util.keyboards import main_menu


# @dp.message_handler(commands=['help'], state=None)
# @checking.check_registration
async def command_help(message: types.Message):
    """Check user in database and send message with password or welcome message."""
    await message.answer('Help. \n Here you can find help information\n And it will be here soon', reply_markup=main_menu)
    logger.info(
        f'Entry to help handler user {message.from_user.first_name} (id:{message.from_user.id})')

    logger.warning(
            f'Exit from help handler user {message.from_user.first_name} (id:{message.from_user.id})')


def register_handlers_help(dp: Dispatcher):
    dp.register_message_handler(command_help, commands=['help'])


if __name__ == '__main__':
    pass
