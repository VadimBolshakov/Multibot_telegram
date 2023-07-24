from admin.logsetting import logger
from json import load
import random
import os


def jokes_dict(quantity: int = 10) -> dict[int, str] | str:
    """Get jokes from json-file and return dict of jokes."""
    try:
        file_jokes = os.path.abspath(f'./src/jokes/jokes_ru.json')
        with open(file_jokes, 'r') as file:
            load_jokes = load(file)

    except FileNotFoundError as e:
        logger.exception(f'JokeError: {str(e)}')
        return 'Sorry, joke not found'

    jokes = {}

    for i in random.sample(range(1, 124156), quantity):
        jokes[i] = load_jokes.get(str(i))

    return jokes


if __name__ == '__main__':
    print(jokes_dict(10))
