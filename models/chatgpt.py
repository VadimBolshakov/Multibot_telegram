"""ChatGPT model.
    Response request from chatgpthandler.py.
    Forms a request to the ChatGPT API.
    Get answer from ChatGPT API via https://api.openai.com/v1/completions.
    Send answer to chatgptview as dict or string.
"""
import asyncio
from json import JSONDecodeError
from typing import Optional

import aiohttp

from admin import exeptions as ex
from create import GPT_API_KEY, db, logger


async def get_chatgpt(prompt: str) -> Optional[dict]:
    """Get answer from ChatGPT API.

    :param prompt: request from user
    :type prompt: str

    :raises ex.ResponseStatusError: if response status not 200
    :raises JSONDecodeError: if response not json
    :raises aiohttp.ClientConnectorError: if connection error

    :return: answer from ChatGPT API
    :rtype: Optional[dict]
    """
    json = {
        'model': 'text-davinci-003',  # 'davinci' is the default
        'prompt': prompt,
        'max_tokens': 500,
        'temperature': 0.6,
        # "top_p": 0.7,
        'frequency_penalty': 0.2,
        'presence_penalty': 0.3,
    }

    url = "https://api.openai.com/v1/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT_API_KEY}"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json, headers=headers) as response:
                if response.status != 200:
                    raise ex.ResponseStatusError(response.status)

                data_chatgpt = await response.json()

                return data_chatgpt

    except (aiohttp.ClientConnectorError, JSONDecodeError, ex.ResponseStatusError) as e:
        logger.exception(f'ChatgptError: {str(e)}')
        return None

    #     response_chatgpt = requests.post(url=url, json=json, headers=headers)
    #
    #     if not response_chatgpt:
    #         raise ex.ResponseStatusError(response_chatgpt.status_code)
    #
    #     data_chatgpt = response_chatgpt.json()
    #     return data_chatgpt
    #
    # except (requests.RequestException, ex.ResponseStatusError) as e:
    #     logger.exception(f'Chatgpt: {str(e)}')
    #     return None


async def chatgpt_dict(user_id: int, first_name: str, prompt: str) -> dict[str, str] | str:
    """Return dict with answer from ChatGPT API or error str if answer is not response.

    :param user_id: user id
    :type user_id: int
    :param first_name: user first name
    :type first_name: str
    :param prompt: request from user
    :type prompt: str

    :return: dict with answer from ChatGPT API
    :rtype: dict[str, str] | str
    """
    data_chatgpt = await get_chatgpt(prompt)

    if data_chatgpt is None:
        logger.warning(f'ChatgptError. User {first_name} (id:{user_id})')
        await db.add_request_db(user_id=user_id, type_request='chatgpt', num_tokens=0, status_request=False)
        return 'Error. Can\'t get answer from ChatGPT API.'

    _chatgpt = {'answer': data_chatgpt['choices'][0]['text']}

    await db.add_request_db(user_id=user_id,
                            type_request='chatgpt',
                            num_tokens=data_chatgpt['usage']['total_tokens'],
                            status_request=True)
    logger.info(
        f'Exit from chatgpt model user {first_name} (id:{user_id})')

    return _chatgpt


if __name__ == '__main__':
    print(asyncio.run(chatgpt_dict(user_id=111, first_name='test', prompt='Hello, how are you?')))
