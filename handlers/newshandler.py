"""Handler for news."""

from aiogram import types
from create import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from databases import database
from util.keyboards import main_menu, category_menu
from view import newsview, quoteview
from models import news, quote
from admin.logsetting import logger


class NewsFSM(StatesGroup):
    category = State()
    query = State()


# @dp.message_handler(state=None)
async def select_category(message: types.Message):
    """Select category and set FSM state."""
    await message.answer('Select category or press "Cancel" for exit', reply_markup=category_menu)
    """Set FSM state."""
    await NewsFSM.category.set()


@dp.message_handler(state=NewsFSM.category)
async def input_category(message: types.Message, state: FSMContext):
    """Set category and suggest input text to query."""
    async with state.proxy() as data:
        data['category'] = message.text.lower().split()
    if data['category'][0] in ('business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'):
        msg = await message.answer('Wait a second, please', reply_markup=types.ReplyKeyboardRemove())
        category = data['category'][0]
        country = await database.get_user_lang_db(user_id=int(message.from_user.id))
        # lang = await database.get_user_lang_db(user_id=int(message.from_user.id))
        answer = newsview.news_view(news_dictionary=await news.news_dict(message.from_user.id,
                                                                         message.from_user.first_name,
                                                                         country=country,
                                                                         category=category))

        if len(answer) > 4096:
            for x in range(0, len(answer), 4096):
                await message.answer(answer[x:x + 4096])
        else:
            await message.answer(answer)

        await msg.delete()

    else:
        await message.answer('I don\'t understand you', reply_markup=types.ReplyKeyboardRemove())
        logger.info(
            f'Cancel news handler user {message.from_user.first_name} (id:{message.from_user.id})')
    await state.finish()
    await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)


# @dp.message_handler(state=NewsFSM.query)
# async def input_translator(message: Message, state: FSMContext):
#     """Get query and send news message."""
#     async with state.proxy() as data:
#         data['query'] = message.text.split()
#
#     data = await state.get_data()
#     category = data['category'][0]
#     # query = data['query'][0]
#     msg = await message.answer('Wait a second, please')
#     answer = newsview.news_view(news_dict=news.news_dict(country='ru', category=category, query=query))
#
#     if len(answer) > 4096:
#         for x in range(0, len(answer), 4096):
#             await message.answer(answer[x:x + 4096])
#     else:
#         await message.answer(answer)
#
#     await msg.delete()
#     await state.finish()
#     await message.answer(quoteview.quote_view(quote.quote_dict(lang='ru')), reply_markup=main_menu)


if __name__ == '__main__':
    pass
