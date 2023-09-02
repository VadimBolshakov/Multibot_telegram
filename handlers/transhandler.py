"""Handler for translate function."""

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from create import dp, logger, i18n
from models import translator, quote
from util.keyboards import create_menu_inline
from view import translateview, quoteview

_ = i18n.gettext


class TranslateFSM(StatesGroup):
    """Class for translate FSM.

    Args:
        StatesGroup (StatesGroup):Basis class for translate FSM.

    Attributes:
        target (State): State for select target language.
        translator (State): State for input text for translate.
    """

    target = State()
    translator = State()


# @dp.message_handler(state=None)
async def select_language(message: types.Message, user_id: int) -> None:
    """Select into language and set FSM state.

    :param message: Message object from user.
    :type message: Message
    :param user_id: User id.
    :type user_id: int

    :return: None
    :rtype: None
    """
    await message.answer(_('Select into language or press "Cancel" for exit'),
                         reply_markup=await create_menu_inline('translate_menu', user_id=user_id))
    """Set FSM state."""
    await TranslateFSM.target.set()


@dp.callback_query_handler(text=['en', 'ru', 'uk', 'de', 'fr', 'it', 'es', 'el', 'pl', 'pt', 'tr', 'ar', 'ja', 'ch'],
                           state=TranslateFSM.target)
async def select_target(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Set target and suggest input text to translate.

    :param callback_query: CallbackQuery object from inline button click (callback_data equal name of target language)
    :type callback_query: CallbackQuery
    :param state: FSM state.
    :type state: FSMContext

    :return: None
    :rtype: None
    """
    await callback_query.answer(_('Please, wait'))
    async with state.proxy() as data:
        data['target'] = callback_query.data
    await callback_query.message.answer(_('Enter text for translate:'), reply_markup=ReplyKeyboardRemove())
    await TranslateFSM.translator.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=TranslateFSM.translator)
async def input_translator(message: types.Message, state: FSMContext) -> None:
    """Translate text and send message with translate text.

    :param message: Message object from user.
    :type message: Message
    :param state: FSM state.
    :type state: FSMContext

    :return: None
    :rtype: None
    """
    async with state.proxy() as data:
        data['text'] = message.text
    data = await state.get_data()
    target = data['target']
    text = data['text']

    if text is not None:
        msg = await message.answer(_('Please, Wait a second.....'))
        translate_text = await translator.translate_dict(message.from_user.id, message.from_user.first_name, target, text)
        await message.answer(translateview.translate_view(translate_text), reply_markup=ReplyKeyboardRemove())
        await msg.delete()
    else:
        await message.answer(_('I don\'t understand you'), reply_markup=ReplyKeyboardRemove())
        logger.info(
            f'Cancel translate handler user {message.from_user.first_name} (id:{message.from_user.id})')
    # await state.reset_state(with_data=False)
    await state.finish()
    await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)),
                         reply_markup=await create_menu_inline('main_menu', user_id=message.from_user.id))


if __name__ == '__main__':
    pass
