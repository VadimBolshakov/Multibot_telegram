from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create import dp, db, logger, i18n
from util.keyboards import create_menu_inline

_ = i18n.gettext


class ChangeLangFSM(StatesGroup):
    language = State()


# @dp.message_handler(commands=['lang'])
async def select_lang(message: types.Message):
    """Change language."""
    logger.info(
        f'Entry to select language handler user {message.from_user.first_name} (id:{message.from_user.id})')
    await message.answer(_('Your are currently language : {lang} \n'
                         ' Choose language').format(lang=await db.get_user_lang_db(message.from_user.id)),
                         reply_markup=await create_menu_inline('language_menu',
                                                               language=await db.get_user_lang_db(message.from_user.id)))
    await ChangeLangFSM.language.set()


@dp.callback_query_handler(text=['en', 'ru'], state=ChangeLangFSM.language)
async def change_lang(callback_query: types.CallbackQuery, state: FSMContext):
    """Change language."""
    await callback_query.answer(_('Please, wait'))
    async with state.proxy() as data:
        data['language'] = callback_query.data
    chan_lang = await db.up_user_lang_db(callback_query.from_user.id, data['language'])
    if chan_lang:
        await callback_query.message.answer(_('Language changed to {lang}').format(lang=data['language']),
                                            reply_markup=types.ReplyKeyboardRemove())
        logger.info(f'Language changed to {data["language"]} user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    else:
        await callback_query.message.answer(_('Language not changed'))
    await state.finish()
    logger.info(
        f'Exit from select language handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.message.answer(_('Welcome to Main menu'),
                                        reply_markup=await create_menu_inline('main_menu', language=data['language']))


def register_handlers_change_lang():
    """Register handlers for change language."""
    dp.register_message_handler(select_lang, commands=['lang'])
    dp.register_callback_query_handler(change_lang, text=['en', 'ru'], state=ChangeLangFSM.language)


if __name__ == '__main__':
    pass
