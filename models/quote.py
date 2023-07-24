import requests
from json import JSONDecodeError
# from json import dump
from admin.logsetting import logger
from typing import Optional
from admin import exeptions as ex


def get_quote(lang: str = 'en') -> Optional[dict[str, str | None]]:
    """Get quote from http://forismatic.com/ru/api/."""
    params_quote = {
        'method': 'getQuote',
        'format': 'json',
        'lang': lang,
        'key': 173259,
    }

    url_quote = 'http://api.forismatic.com/api/1.0/'
    try:
        response_quote = requests.get(url=url_quote, params=params_quote)

        if not response_quote:
            raise ex.ResponseStatusError(response_quote.status_code)

        data_quote = response_quote.json()
        # with open('quote.json', 'w') as file:
        #         dump(data_news, file, indent=4, ensure_ascii=False)
        return data_quote

    except (requests.RequestException, JSONDecodeError, ex.ResponseStatusError) as e:
        logger.exception(f'QuoteError: {str(e)}')
        return None


def quote_dict(lang) -> dict[str, str | None] | str:
    """Return quote."""
    _quote = get_quote(lang)
    if _quote is None:
        return 'Error: quote not found'
    else:
        _quote_dict = {'quoteText': _quote['quoteText'], 'quoteAuthor': _quote['quoteAuthor']}
    return _quote_dict


if __name__ == '__main__':
    print(quote_dict('ru'))
