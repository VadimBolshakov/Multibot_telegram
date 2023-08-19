from aiogram import Dispatcher, types
from create import logger, db
from util.keyboards import main_menu


# @dp.message_handler(commands=['help'], state=None)
# @checking.check_registration
async def command_help(message: types.Message):
    """Check user in database and send message with password or welcome message."""
    await message.answer('Help. \n Here11111 you can find help information\n And it will be here soon', reply_markup=main_menu)
    user = await db.get_user_db(user_id=message.from_user.id)
    print(user)
    await message.answer(f'User {user.get("firstname")} (id:{user.get("userid")}, '
                         f'status admin: {user.get("statusadmin")}, is banned: {user.get("is_banned")})'
                         f'language: {user.get("languageuser")}')
    lang = await db.get_user_lang_db(user_id=message.from_user.id)
    logger.info(
        f'Entry to help handler user {message.from_user.first_name} (id:{message.from_user.id})')

    logger.warning(
            f'Exit from help handler user {message.from_user.first_name} (id:{message.from_user.id})')


def register_handlers_help(dp: Dispatcher):
    dp.register_message_handler(command_help, commands=['help'])


if __name__ == '__main__':
    pass
