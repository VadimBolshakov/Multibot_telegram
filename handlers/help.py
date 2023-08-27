from aiogram import Dispatcher, types

from create import logger, i18n, db
from util.keyboards import create_menu_inline

_ = i18n.gettext


# @dp.message_handler(commands=['help'], state=None)
# @checking.check_registration
async def command_help(message: types.Message):
    """Check user in database and send message with password or welcome message."""
    lang = await db.get_user_lang_db(user_id=message.from_user.id)
    file_name = './src/help/help_' + lang + '.txt'
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        logger.warning('Help file not found')
        return

    logger.info(
        f'Entry to help handler user {message.from_user.first_name} (id:{message.from_user.id})')

    await message.answer(text, reply_markup=await create_menu_inline('main_menu', language=lang))

    logger.info(
        f'Exit from help handler user {message.from_user.first_name} (id:{message.from_user.id})')


def register_handlers_help(dp: Dispatcher):
    dp.register_message_handler(command_help, commands=['help'])


if __name__ == '__main__':
    pass
