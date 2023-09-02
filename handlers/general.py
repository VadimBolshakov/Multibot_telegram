"""General handlers."""

import datetime

from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove, CallbackQuery

from create import bot, logger, i18n
from handlers import maphandler, transhandler, weathandler, newshandler, chatgpthandler
from models import currencies, quote, jokes
from util.keyboards import create_menu_inline
from view import currencyview, quoteview, jokesview

_ = i18n.gettext


# from aiogram.contrib.middlewares.i18n import I18nMiddleware


# @dp.callback_query_handler(text='weather')
async def weather(callback_query: CallbackQuery) -> None:
    """Weather handler.

    :param callback_query: CallbackQuery object from inline button click (callback_data='weather')
    :type callback_query: CallbackQuery

    :return: None
    :rtype: None
    """
    logger.info(
        f'Entry to weather handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer(_('Please, wait'))
    await weathandler.select_location(callback_query.message, callback_query.from_user.id)


# @dp.callback_query_handler(text='maps')
async def maps(callback_query: CallbackQuery) -> None:
    """Map handler.

    :param callback_query: CallbackQuery object from inline button click (callback_data='maps')
    :type callback_query: CallbackQuery

    :return: None
    :rtype: None
    """
    logger.info(
        f'Entry to maps handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer(_('Please, wait'))
    await maphandler.select_location(callback_query.message, callback_query.from_user.id)


# @dp.callback_query_handler(text='translate')
async def translate(callback_query: CallbackQuery) -> None:
    """Translate handler.

    :param callback_query: CallbackQuery object from inline button click (callback_data='translate')
    :type callback_query: CallbackQuery

    :return: None
    :rtype: None
    """
    logger.info(
        f'Entry to translate handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer(_('Please, wait'))
    await transhandler.select_language(callback_query.message, callback_query.from_user.id)


# @dp.callback_query_handler(text='currency')
async def currency(callback_query: CallbackQuery) -> None:
    """Currency handler.

    :param callback_query: CallbackQuery object from inline button click (callback_data='currency')
    :type callback_query: CallbackQuery

    :return: None
    :rtype: None
    """
    logger.info(
        f'Entry to currency_ru handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await bot.answer_callback_query(callback_query.id, _('Please, wait'))
    date_now = datetime.datetime.now()
    currencies_dict = await currencies.currencies_dict(callback_query.from_user.id, callback_query.from_user.first_name,
                                                       date_now)
    await callback_query.message.answer(currencyview.currency_view(date_now.strftime('%d-%m-%Y %H:%M'), currencies_dict))
    await callback_query.message.answer(quoteview.quote_view(await quote.quote_dict(callback_query.from_user.id)),
                                        reply_markup=await create_menu_inline('main_menu', user_id=callback_query.from_user.id))


# @dp.callback_query_handler(text='news')
async def new(callback_query: CallbackQuery) -> None:
    """News handler.

    :param callback_query: CallbackQuery object from inline button click (callback_data='news')
    :type callback_query: CallbackQuery

    :return: None
    :rtype: None
    """
    logger.info(
        f'Entry to news handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer(_('Please, wait'))
    await newshandler.select_category(callback_query.message, callback_query.from_user.id)


# @dp.callback_query_handler(text='jokes')
async def joke(callback_query: CallbackQuery) -> None:
    """Jokes handler.

    :param callback_query: CallbackQuery object from inline button click (callback_data='jokes')
    :type callback_query: CallbackQuery

    :return: None
    :rtype: None
    """
    logger.info(f'Entry to jokes handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer(_('Please, wait'))
    jokes_dict = await jokes.jokes_dict(callback_query.from_user.id, callback_query.from_user.first_name, quantity=15)
    await callback_query.message.answer(jokesview.jokes_view(jokes_dict),
                                        reply_markup=await create_menu_inline('main_menu', user_id=callback_query.from_user.id))


# @dp.callback_query_handler(text='chat_gpt')
async def chat_gpt(callback_query: CallbackQuery) -> None:
    """Chat GPT handler.

    :param callback_query: CallbackQuery object from inline button click (callback_data='chat_gpt')
    :type callback_query: CallbackQuery

    :return: None
    :rtype: None
    """
    logger.info(
        f'Entry to chat_gpt handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer(_('Please, wait'))
    await callback_query.message.answer(_('Ask me a everything you want'))
    await chatgpthandler.select_question(callback_query.message)


# @dp.callback_query_handler(text='cancel', state='*')
async def cancel(callback_query: CallbackQuery, state: FSMContext) -> None:
    """Cancel and exit from FSM state.

    :param callback_query: CallbackQuery object from inline button click (callback_data='cancel')
    :type callback_query: CallbackQuery
    :param state: FSM any state
    :type state: FSMContext

    :return: None
    :rtype: None
    """
    await callback_query.answer(_('Please, wait'))
    await callback_query.message.answer(_('Cancel'), reply_markup=ReplyKeyboardRemove())
    await state.finish()
    logger.info(
        f'Cancel weather handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.message.answer(quoteview.quote_view(await quote.quote_dict(callback_query.from_user.id)),
                                        reply_markup=await create_menu_inline('main_menu', user_id=callback_query.from_user.id))


# @dp.message_handler(content_types=ContentTypes.TEXT, state='*')
async def text(message: Message, state: FSMContext) -> None:
    """Text handler.

    :param message: Message object from user
    :type message: Message
    :param state: FSM any state
    :type state: FSMContext

    :return: None
    :rtype: None
    """
    await message.answer(_('Hi, you typed {text}').format(text=message.text), reply_markup=ReplyKeyboardRemove())
    await state.finish()


# @dp.message_handler(content_types=types.ContentType.ANY, state='*')
async def unknown_message(message: Message, state: FSMContext) -> None:
    """Unknown message handler.

    :param message: Message object from user
    :type message: Message
    :param state: FSM any state
    :type state: FSMContext

    :return: None
    :rtype: None
    """
    await message.answer(_('I only understand text'), reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)),
                         reply_markup=await create_menu_inline('main_menu', user_id=message.from_user.id))


def register_handlers_general(dp: Dispatcher) -> None:
    """Register general handlers.

    :param dp: Dispatcher object
    :type dp: Dispatcher

    :return: None
    :rtype: None
    """
    dp.register_callback_query_handler(weather, text='weather')
    dp.register_callback_query_handler(maps, text='maps')
    dp.register_callback_query_handler(new, text='news')
    dp.register_callback_query_handler(translate, text='translate')
    dp.register_callback_query_handler(currency, text='currency')
    dp.register_callback_query_handler(joke, text='jokes')
    dp.register_callback_query_handler(chat_gpt, text='chat_gpt')
    dp.register_callback_query_handler(cancel, text='cancel', state='*')
    dp.register_message_handler(text, content_types=ContentTypes.TEXT, state='*')
    dp.register_message_handler(unknown_message, content_types=ContentTypes.ANY, state='*')
