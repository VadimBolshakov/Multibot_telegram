import asyncio
import aiohttp
from json import JSONDecodeError
from admin import exeptions as ex
from admin.logsetting import logger
from databases import database
from create import GPT_API_KEY
from typing import Optional


async def get_chatgpt(prompt: str) -> Optional[dict]:
    """Get answer from ChatGPT API."""
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
    """Return dict with answer from ChatGPT API."""
    data_chatgpt = await get_chatgpt(prompt)

    if data_chatgpt is None:
        logger.warning(f'ChatgptError. User {first_name} (id:{user_id})')
        await database.add_request_db(user_id=user_id, type_request='chatgpt', num_tokens=0, status_request=False)
        return 'Error. Can\'t get answer from ChatGPT API.'

    _chatgpt = {'answer': data_chatgpt['choices'][0]['text']}

    await database.add_request_db(user_id=user_id,
                                  type_request='chatgpt',
                                  num_tokens=data_chatgpt['usage']['total_tokens'],
                                  status_request=True)
    logger.info(
        f'Exit from chatgpt model user {first_name} (id:{user_id})')

    return _chatgpt


if __name__ == '__main__':
    print(asyncio.run(chatgpt_dict(user_id=111, first_name='test', prompt='Hello, how are you?')))

