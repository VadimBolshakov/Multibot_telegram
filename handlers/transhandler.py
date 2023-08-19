"""Handler for translate function."""

from aiogram import types
from create import dp, logger
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from util.keyboards import main_menu, translate_menu
from view import translateview, quoteview
from models import translator, quote


class TranslateFSM(StatesGroup):
    target = State()
    translator = State()


# @dp.message_handler(state=None)
async def select_language(message: types.Message):
    """Select into language and set FSM state."""
    await message.answer('Select into language or press "Cancel" for exit', reply_markup=translate_menu)
    """Set FSM state."""
    await TranslateFSM.target.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=TranslateFSM.target)
async def input_target(message: types.Message, state: FSMContext):
    """Set target and suggest input text to translate."""
    language_code: dict = {'English': 'en',
                           'Russian': 'ru',
                           'Ukrainian': 'uk',
                           'German': 'de',
                           'French': 'fr',
                           'Italian': 'it',
                           'Spanish': 'es',
                           'Greek': 'el',
                           'Polish': 'pl',
                           'Portuguese': 'pt',
                           'Turkish': 'tr',
                           'Arabic': 'ar',
                           'Japanese': 'ja',
                           'Chinese': 'zh'}

    async with state.proxy() as data:
        data['target'] = language_code.get(message.text.split()[0])
    if data['target'] is not None:
        await message.answer('Enter text for translate:', reply_markup=ReplyKeyboardRemove())
        await TranslateFSM.translator.set()
    else:
        await message.answer('I don\'t understand you', reply_markup=ReplyKeyboardRemove())
        await state.finish()
        logger.info(
            f'Cancel translate handler user {message.from_user.first_name} (id:{message.from_user.id})')

        await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)


@dp.message_handler(content_types=types.ContentType.TEXT, state=TranslateFSM.translator)
async def input_translator(message: types.Message, state: FSMContext):
    """Translate text and send message with translate text."""
    async with state.proxy() as data:
        data['text'] = message.text
    data = await state.get_data()
    target = data['target']
    text = data['text']

    if text is not None:
        msg = await message.answer('Please, Wait a second.....')
        translate_text = await translator.translate_dict(message.from_user.id, message.from_user.first_name, target, text)
        await message.answer(translateview.translate_view(translate_text), reply_markup=ReplyKeyboardRemove())
        await msg.delete()
    else:
        await message.answer('I don\'t understand you', reply_markup=ReplyKeyboardRemove())
        logger.info(
            f'Cancel translate handler user {message.from_user.first_name} (id:{message.from_user.id})')
    # await state.reset_state(with_data=False)
    await state.finish()
    await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)


if __name__ == '__main__':
    pass
