"""Create dict of jokes from json-file, according to the user's language.
    Return dict of jokes.
"""
import asyncio
import os
import random
from collections import defaultdict
from json import load

from create import db, logger


async def jokes_dict(user_id: int, first_name: str, quantity: int = 9) -> dict[int, str] | str:
    """Get jokes from json-file and return dict of jokes or error str if jokes is None.

    :param user_id: user id
    :type user_id: int
    :param first_name: user first name
    :type first_name: str
    :param quantity: quantity of jokes, defaults to 9
    :type quantity: int, optional

    :return: dict of jokes
    :rtype: dict[int, str] | str
    """
    lang = await db.get_user_lang_db(user_id=user_id)

    if lang == 'ru':
        file_jokes = os.path.abspath(f'./src/jokes/jokes_ru.json')
        total_quantity = 124156

    else:
        return 'Sorry, joke not found'
        # file_jokes = os.path.abspath(f'./src/jokes/jokes_en.json')
        # total_quantity = 194553

    try:
        with open(file_jokes, 'r') as file:
            load_jokes = load(file)

    except FileNotFoundError as e:
        logger.exception(f'JokeError: {str(e)}. User {first_name} (id:{user_id})')
        await db.add_request_db(user_id=user_id, type_request='jokes', num_tokens=0, status_request=False)
        return 'Sorry, joke not found'

    jokes = defaultdict(str)

    for i in random.sample(range(1, total_quantity), quantity):
        intermed_joke = load_jokes.get(str(i))
        if len(intermed_joke) < 256:
            jokes[i] = intermed_joke
        # jokes[i] = load_jokes.get(str(i))

    await db.add_request_db(user_id=user_id, type_request='jokes', num_tokens=0, status_request=True)
    logger.info(
        f'Exit from jokes model user {first_name} (id:{user_id})')

    return jokes


if __name__ == '__main__':
    print(asyncio.run(jokes_dict(user_id=111, first_name='test', quantity=10)))
