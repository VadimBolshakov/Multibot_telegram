"""Handler for chat_gpt."""

from aiogram import types
from create import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from util.keyboards import main_menu
from view import chatgptview, quoteview
from models import chatgpt, quote
from admin.logsetting import logger


class NewsFSM(StatesGroup):
    question = State()


# @dp.message_handler(state=None)
async def select_question(message: types.Message):
    """Select question and set FSM state."""
    await message.answer('Input your question or type "q" ("й") for exit')
    """Set FSM state."""
    await NewsFSM.question.set()


@dp.message_handler(state=NewsFSM.question)
async def input_question(message: types.Message, state: FSMContext):
    """Get some question and request an answer by ChatGPT."""
    async with state.proxy() as data:
        data['question'] = message.text
    if data['question'] != 'q' and data['question'] != 'Q' and data['question'] != 'й' and data['question'] != 'Й':
        msg = await message.answer('Wait a second, please')
        question = data['question']
        await message.answer(chatgptview.chatgpt_view(await chatgpt.chatgpt_dict(message.from_user.id,
                                                                                 message.from_user.first_name,
                                                                                 prompt=question)))
        await msg.delete()

    else:
        await message.answer('I don\'t understand you')
        logger.info(
            f'Cancel chatgpt handler user {message.from_user.first_name} (id:{message.from_user.id})')
    await state.finish()
    await message.answer(quoteview.quote_view(await quote.quote_dict(message.from_user.id)), reply_markup=main_menu)


if __name__ == '__main__':
    pass
