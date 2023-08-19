"""Translates text into the target language.

Used this snippet from https://cloud.google.com/translate/docs/basic/quickstart
Target must be an ISO 639-1 language code.
See https://g.co/cloud/translate/v2/translate-reference#supported_languages
"""
import asyncio
import aiohttp
from json import JSONDecodeError

from create import TOKEN_GOOGLE_TRANSLATE, db, logger
from admin import exeptions as ex
from typing import Optional


async def get_language(text_to_translate: str) -> Optional[dict[str]]:
    """Detects the text's language using the Google Translate API."""

    url = "https://translation.googleapis.com/language/translate/v2/detect"
    params = {
        "q": text_to_translate,
        'key': TOKEN_GOOGLE_TRANSLATE,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise ex.ResponseStatusError(response.status)

                data_language = await response.json()

                return data_language

    except (aiohttp.ClientConnectorError, JSONDecodeError, ex.ResponseStatusError) as e:
        logger.exception(f'DetectError: {str(e)}')
        return None


async def get_translate(language_target: str, text_to_translate: str) -> Optional[dict[str]]:
    """Translates text from one language to another using the Google Translate API."""

    if isinstance(text_to_translate, bytes):
        text_to_translate = text_to_translate.decode("utf-8")

    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "q": text_to_translate,
        # "source": 'en',
        "target": language_target,
        'key': TOKEN_GOOGLE_TRANSLATE,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise ex.ResponseStatusError(response.status)

                data_translate = await response.json()

                return data_translate

    except (aiohttp.ClientConnectorError, JSONDecodeError, ex.ResponseStatusError) as e:
        logger.exception(f'TranslateError: {str(e)}')
        return None


async def translate_dict(user_id: int, first_name: str, language_target: str, text_to_translate: str) -> dict[str, str] | str:
    """Get translate from Google Translate API and return dict."""
    data_translate = await get_translate(language_target, text_to_translate)

    if data_translate is None:
        logger.warning(f'TranslateError. User {first_name} (id:{user_id})')
        await db.add_request_db(user_id=user_id, type_request='translate', num_tokens=0, status_request=False)
        return 'Sorry, but I have not translate it. Error: translate not found'

    _translate_dict = {'translate_text': data_translate['data']['translations'][0]['translatedText'],
                       'language': data_translate['data']['translations'][0]['detectedSourceLanguage']}

    await db.add_request_db(user_id=user_id, type_request='translate', num_tokens=0, status_request=True)
    logger.info(
        f'Exit from translate model user {first_name} (id:{user_id})')

    return _translate_dict


if __name__ == '__main__':
    text = asyncio.run(translate_dict(user_id=111, first_name='test', language_target='ru', text_to_translate='Hello, world! I am here'))
    print(text)
    print(get_language(text_to_translate='Hello, world! I am here'))
