"""Handler for news."""
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from create import dp, db, logger, i18n
from models import news, quote
from util.keyboards import create_menu_inline
from view import newsview, quoteview

_ = i18n.gettext


class NewsFSM(StatesGroup):
    """Class for news FSM.

    Args:
        StatesGroup (StatesGroup):Basis class for news FSM.

    Attributes:
        category (State): State for select category.
        query (State): State for input query.
    """

    category = State()
    query = State()


# @dp.message_handler(state=None)
async def select_category(message: types.Message, user_id: int) -> None:
    """Select category and set FSM state.

    :param message: Message object from user.
    :type message: Message
    :param user_id: User id.
    :type user_id: int

    :return: None
    :rtype: None
    """
    await message.answer(_('Select category or press "Cancel" for exit'),
                         reply_markup=await create_menu_inline('news_category_menu',
                                                               user_id=user_id))
    """Set FSM state."""
    await NewsFSM.category.set()


@dp.callback_query_handler(text=['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'],
                           state=NewsFSM.category)
async def input_category(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Set category and suggest input text to query.

    :param callback_query: CallbackQuery object from inline button click (callback_data equal name of category)
    :type callback_query: CallbackQuery
    :param state: FSM state.
    :type state: FSMContext

    :return: None
    :rtype: None
    """
    await callback_query.answer(_('Please, wait'))
    async with state.proxy() as data:
        data['category'] = callback_query.data
    await callback_query.message.answer(_('Input text to query (ex. football) or press "Cancel" for exit\n'
                                          'If you want to see all news (without query), input "All"\n'
                                          'Note. for English is a better input query, otherwise, world news will be shown.'),
                                        reply_markup=types.ReplyKeyboardMarkup(
                                            keyboard=[[types.KeyboardButton('All'), types.KeyboardButton('Cancel')]], resize_keyboard=True))
    await NewsFSM.next()


@dp.message_handler(state=NewsFSM.query)
async def input_query(message: types.Message, state: FSMContext) -> None:
    """Set query and send news.

    :param message: Message object from user.
    :type message: Message
    :param state: FSM state.
    :type state: FSMContext

    :return: None
    :rtype: None
    """
    async with state.proxy() as data:
        data['query'] = message.text.lower().split()
    if data['query'][0] != 'cancel':
        msg = await message.answer(_('Wait a second, please'), reply_markup=types.ReplyKeyboardRemove())
        category = data['category']
        country = await db.get_user_lang_db(user_id=int(message.from_user.id))
        if country == 'en':
            country = ''
        query = data['query'][0]
        if query == 'all':
            query = None
        news_dictionary = await news.news_dict(message.from_user.id,
                                               message.from_user.first_name,
                                               country=country,
                                               category=category,
                                               query=query)
        await msg.delete()
        for item_news in newsview.news_view(news_dictionary):

            if len(item_news) > 4015:
                for x in range(0, len(item_news), 4015):
                    await message.answer(item_news[x:x + 4015])
            else:
                await message.answer(item_news)

            await sleep(.1)

        logger.info(
            f'Exit News handler user {message.from_user.first_name} (id:{message.from_user.id})')

    else:
        await message.answer(_('I don\'t understand you'), reply_markup=types.ReplyKeyboardRemove())
        logger.info(
            f'Cancel news handler user {message.from_user.first_name} (id:{message.from_user.id})')
    await state.finish()
    await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)),
                         reply_markup=await create_menu_inline('main_menu', user_id=message.from_user.id))


if __name__ == '__main__':
    pass
