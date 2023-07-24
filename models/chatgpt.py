import requests
from admin import exeptions as ex

from admin.logsetting import logger
from create import bot
from databases import database
from create import GPT_API_KEY
from datetime import datetime
from typing import Optional


def get_chatgpt(prompt: str) -> Optional[dict]:
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
        response_chatgpt = requests.post(url=url, json=json, headers=headers)

        if not response_chatgpt:
            raise ex.ResponseStatusError(response_chatgpt.status_code)

        data_chatgpt = response_chatgpt.json()
        return data_chatgpt

    except (requests.RequestException, ex.ResponseStatusError) as e:
        logger.exception(f'Chatgpt: {str(e)}')
        return None


def chatgpt_dict(prompt: str) -> dict[str, str] | str:
    """Return dict with answer from ChatGPT API."""
    data_chatgpt = get_chatgpt(prompt)

    if data_chatgpt is None:
        return 'Error. Can\'t get answer from ChatGPT API.'

    _chatgpt = {'answer': data_chatgpt['choices'][0]['text']}

    return _chatgpt


if __name__ == '__main__':
    print(chatgpt_dict('Hello, how are you?'))
