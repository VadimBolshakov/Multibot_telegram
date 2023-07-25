# This file contains general handlers
from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import Dispatcher, FSMContext
from util.keyboards import main_menu
from models import currencies, quote, jokes
from view import currencyview, quoteview, jokesview
from handlers import maphandler, transhandler, weathandler, newshandler, chatgpthandler
import datetime
from create import bot
from admin.logsetting import logger
from databases import database


# from aiogram.contrib.middlewares.i18n import I18nMiddleware


# @dp.callback_query_handlers(text='weather')
async def weather(callback_query: CallbackQuery):
    logger.info(
        f'Enter in weather handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer('Please, wait')
    await weathandler.select_location(callback_query.message)


# @dp.callback_query_handlers(text='maps')
async def maps(callback_query: CallbackQuery):
    logger.info(
        f'Enter in maps handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer('Please, wait')
    await maphandler.select_location(callback_query.message)


# @dp.callback_query_handlers(text='translate')
async def translate(callback_query: CallbackQuery):
    logger.info(
        f'Enter in translate handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer('Please, wait')
    await transhandler.select_language(callback_query.message)


# @dp.callback_query_handlers(text='currency')
async def currency(callback_query: CallbackQuery):
    logger.info(
        f'Enter in currency handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await bot.answer_callback_query(callback_query.id, 'Please, wait')
    date_now = datetime.datetime.now().strftime("%d-%m-%Y")
    currencies_dict = await currencies.currencies_dict(callback_query.from_user.id, callback_query.from_user.first_name,
                                                       date_now)
    await callback_query.message.answer(currencyview.currency_view(date_now, currencies_dict))
    await callback_query.message.answer(quoteview.quote_view(await quote.quote_dict(callback_query.from_user.id)),
                                        reply_markup=main_menu)


# @dp.callback_query_handlers(text='news')
async def new(callback_query: CallbackQuery):
    logger.info(
        f'Enter in news handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer('Please, wait')
    await newshandler.select_category(callback_query.message)


# @dp.callback_query_handlers(text='jokes')
async def joke(callback_query: CallbackQuery):
    logger.info(f'Enter in joke handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer('Please, wait')
    await callback_query.message.answer(jokesview.jokes_view(await jokes.jokes_dict(callback_query.from_user.id,
                                                                                    callback_query.from_user.first_name,
                                                                                    quantity=15)),
                                        reply_markup=main_menu)
    await database.add_request_db(user_id=callback_query.from_user.id, type_request='joke',
                                  num_tokens=1, status_request=True)
    logger.info(
        f'Exit from joke handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')


# @dp.callback_query_handlers(text='chat_gpt')
async def chat_gpt(callback_query: CallbackQuery):
    logger.info(
        f'Enter in chat_gpt handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer('Please, wait')
    await callback_query.message.answer('Спроси меня что-нибудь')
    await chatgpthandler.select_question(callback_query.message)


# @dp.message_handler(content_types=ContentTypes.TEXT)
async def text(message: Message):
    await message.answer('Pres any key', reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(content_types=types.ContentType.ANY, state='*')
async def unknown_message(message: Message, state: FSMContext):
    """Unknown message handler."""
    await message.answer('I only understand text', reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)


def register_handlers_general(dp: Dispatcher):
    dp.register_callback_query_handler(weather, text='weather')
    dp.register_callback_query_handler(maps, text='maps')
    dp.register_callback_query_handler(new, text='news')
    dp.register_callback_query_handler(translate, text='translate')
    dp.register_callback_query_handler(currency, text='currency')
    dp.register_callback_query_handler(joke, text='jokes')
    dp.register_callback_query_handler(chat_gpt, text='chat_gpt')
    dp.register_message_handler(text, content_types=ContentTypes.TEXT)
    dp.register_message_handler(unknown_message, content_types=ContentTypes.ANY, state='*')
