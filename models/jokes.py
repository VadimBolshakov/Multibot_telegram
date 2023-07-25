import asyncio

from admin.logsetting import logger
from databases import database
from json import load
import random
import os


async def jokes_dict(user_id: int, first_name: str, quantity: int = 10) -> dict[int, str] | str:
    """Get jokes from json-file and return dict of jokes."""
    try:
        file_jokes = os.path.abspath(f'./src/jokes/jokes_ru.json')
        with open(file_jokes, 'r') as file:
            load_jokes = load(file)

    except FileNotFoundError as e:
        logger.exception(f'JokeError: {str(e)}. User {first_name} (id:{user_id})')
        await database.add_request_db(user_id=user_id, type_request='joke', num_tokens=0, status_request=False)
        return 'Sorry, joke not found'

    jokes = {}

    for i in random.sample(range(1, 124156), quantity):
        jokes[i] = load_jokes.get(str(i))

    await database.add_request_db(user_id=user_id, type_request='jokes', num_tokens=0, status_request=True)
    logger.info(
        f'Exit from jokes model user {first_name} (id:{user_id})')

    return jokes


if __name__ == '__main__':
    print(asyncio.run(jokes_dict(user_id=111, first_name='test', quantity=10)))
