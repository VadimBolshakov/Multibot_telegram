import asyncio

import aiohttp
from json import JSONDecodeError
from typing import Optional
from admin import exeptions as ex
from create import db, logger


async def get_quote(lang: str = 'en') -> Optional[dict[str, str | None]]:
    """Get quote from http://forismatic.com/ru/api/."""
    params_quote = {
        'method': 'getQuote',
        'format': 'json',
        'lang': lang,
        'key': 1759,
    }

    url_quote = 'http://api.forismatic.com/api/1.0/'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url_quote, params=params_quote) as response:
                if response.status != 200:
                    raise ex.ResponseStatusError(response.status)

                data_quote = await response.json()

                return data_quote

    except (aiohttp.ClientConnectorError, JSONDecodeError, ex.ResponseStatusError) as e:
        logger.exception(f'QuoteError: {str(e)}')
        return None


async def quote_dict(user_id) -> dict[str, str | None] | str:
    """Return quote."""
    lang = await db.get_user_lang_db(user_id=int(user_id))
    _quote = await get_quote(lang)
    if _quote is None:
        return 'Error: quote not found'
    else:
        _quote_dict = {'quoteText': _quote['quoteText'], 'quoteAuthor': _quote['quoteAuthor']}
    return _quote_dict


if __name__ == '__main__':
    print(asyncio.run(quote_dict('ru')))
