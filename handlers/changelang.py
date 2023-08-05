from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from admin.logsetting import logger
from databases import database
from util.keyboards import language_menu, main_menu


class ChangeLangFSM(StatesGroup):
    language = State()


# @dp.message_handler(commands=['lang'])
async def select_lang(message: types.Message):
    """Change language."""
    logger.info(
        f'Entry to select language handler user {message.from_user.first_name} (id:{message.from_user.id})')
    await message.answer(f'Your are currently language : {await database.get_user_lang_db(message.from_user.id)} \n'
                         f' Choose language', reply_markup=language_menu)
    # await message.answer('Choose language', reply_markup=keyboard_lang)
    await ChangeLangFSM.language.set()


# @dp.message_handler(state=ChangeLangFSM.language)
async def change_lang(message: types.Message, state: FSMContext):
    """Change language."""
    async with state.proxy() as data:
        data['language'] = message.text
    if data['language'] == 'Русский':
        await state.update_data(language='ru')
        await database.up_user_lang_db(message.from_user.id, 'ru')
        await message.answer('Язык изменен на русский / Language changed to Russian', reply_markup=types.ReplyKeyboardRemove())
        logger.info(f'Language changed to Russian user {message.from_user.first_name} (id:{message.from_user.id})')
    elif data['language'] == 'English':
        await state.update_data(language='en')
        await database.up_user_lang_db(message.from_user.id, 'en')
        await message.answer('Language changed to English / Язык изменен на английский', reply_markup=types.ReplyKeyboardRemove())
        logger.info(f'Language changed to English user {message.from_user.first_name} (id:{message.from_user.id})')
    else:
        await message.answer('Язык не изменен / Language not changed')
    await state.finish()
    await message.answer('Главное меню / Main menu', reply_markup=main_menu)


def register_handlers_change_lang(_dp: Dispatcher):
    """Register handlers for change language."""
    _dp.register_message_handler(select_lang, commands=['lang'])
    _dp.register_message_handler(change_lang, state=ChangeLangFSM.language)


if __name__ == '__main__':
    pass
