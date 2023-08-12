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



# from aiogram.contrib.middlewares.i18n import I18nMiddleware


# @dp.callback_query_handlers(text='weather')
async def weather(callback_query: CallbackQuery):
    logger.info(
        f'Entry to weather handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer('Please, wait')
    await weathandler.select_location(callback_query.message)


# @dp.callback_query_handlers(text='maps')
async def maps(callback_query: CallbackQuery):
    logger.info(
        f'Entry to maps handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer('Please, wait')
    await maphandler.select_location(callback_query.message)


# @dp.callback_query_handlers(text='translate')
async def translate(callback_query: CallbackQuery):
    logger.info(
        f'Entry to translate handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer('Please, wait')
    await transhandler.select_language(callback_query.message)


# @dp.callback_query_handlers(text='currency_ru')
async def currency(callback_query: CallbackQuery):
    logger.info(
        f'Entry to currency_ru handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await bot.answer_callback_query(callback_query.id, 'Please, wait')
    date_now = datetime.datetime.now()
    currencies_dict = await currencies.currencies_dict(callback_query.from_user.id, callback_query.from_user.first_name,
                                                       date_now)
    await callback_query.message.answer(currencyview.currency_view(date_now.strftime('%d-%m-%Y %H:%M'), currencies_dict))
    await callback_query.message.answer(quoteview.quote_view(await quote.quote_dict(callback_query.from_user.id)),
                                        reply_markup=main_menu)


# @dp.callback_query_handlers(text='news')
async def new(callback_query: CallbackQuery):
    logger.info(
        f'Entry to news handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer('Please, wait')
    await newshandler.select_category(callback_query.message)


# @dp.callback_query_handlers(text='jokes')
async def joke(callback_query: CallbackQuery):
    logger.info(f'Entry to jokes handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer('Please, wait')
    jokes_dict = await jokes.jokes_dict(callback_query.from_user.id, callback_query.from_user.first_name, quantity=15)
    await callback_query.message.answer(jokesview.jokes_view(jokes_dict), reply_markup=main_menu)


# @dp.callback_query_handlers(text='chat_gpt')
async def chat_gpt(callback_query: CallbackQuery):
    logger.info(
        f'Entry to chat_gpt handler user {callback_query.from_user.first_name} (id:{callback_query.from_user.id})')
    await callback_query.answer('Please, wait')
    await callback_query.message.answer('Ask me a everything you want')
    await chatgpthandler.select_question(callback_query.message)


# @dp.message_handler(content_types=ContentTypes.TEXT)
async def text(message: Message):
    await message.answer(f'Hi, you typed {message.text}', reply_markup=ReplyKeyboardRemove())


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
    dp.register_callback_query_handler(currency, text='currency_ru')
    dp.register_callback_query_handler(joke, text='jokes')
    dp.register_callback_query_handler(chat_gpt, text='chat_gpt')
    dp.register_message_handler(text, content_types=ContentTypes.TEXT)
    dp.register_message_handler(unknown_message, content_types=ContentTypes.ANY, state='*')
