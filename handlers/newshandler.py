"""Handler for news."""
from asyncio import sleep
from aiogram import types
from create import dp, db, logger, i18n
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from util.keyboards import main_menu, news_category_menu, news_query_menu
from view import newsview, quoteview
from models import news, quote

_ = i18n.gettext


class NewsFSM(StatesGroup):
    category = State()
    query = State()


# @dp.message_handler(state=None)
async def select_category(message: types.Message):
    """Select category and set FSM state."""
    await message.answer(_('Select category or press "Cancel" for exit'), reply_markup=news_category_menu)
    """Set FSM state."""
    await NewsFSM.category.set()


@dp.message_handler(state=NewsFSM.category)
async def input_category(message: types.Message, state: FSMContext):
    """Set category and suggest input text to query."""
    async with state.proxy() as data:
        data['category'] = message.text.lower().split()
    if data['category'][0] in ('business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'):
        await message.answer(_('Input text to query (ex. football) or press "Cancel" for exit\n'
                               'If you want to see all news (without query), input "All"\n'
                               'Note. for English is a better input query, otherwise, world news will be shown.'),
                             reply_markup=news_query_menu)
        await NewsFSM.next()
    else:
        await message.answer(_('I don\'t understand you'), reply_markup=types.ReplyKeyboardRemove())
        logger.info(
            f'Cancel news handler user {message.from_user.first_name} (id:{message.from_user.id})')
        await state.finish()
        await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)


@dp.message_handler(state=NewsFSM.query)
async def input_query(message: types.Message, state: FSMContext):
    """Set query and send news."""
    async with state.proxy() as data:
        data['query'] = message.text.lower().split()
    if data['query'][0] != 'cancel':
        msg = await message.answer(_('Wait a second, please'), reply_markup=types.ReplyKeyboardRemove())
        category = data['category'][0]
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
    await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)


if __name__ == '__main__':
    pass
