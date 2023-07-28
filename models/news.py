import asyncio

import requests
from json import JSONDecodeError
from databases import database
from admin.logsetting import logger
from create import TOKEN_NEWSAPI
from typing import Optional
from admin import exeptions as ex
import datetime


def get_news(country: str = 'en',
             sources: str = 'bbc-news',
             category: str = 'general',
             query: Optional[str] = None,
             page: int = 1) -> Optional[dict[str, str | int | float | list[dict[str, str | None]]]]:
    """Get news from NewsAPI API."""
    params_newsapi = {
        'apiKey': TOKEN_NEWSAPI,
        'country': country,
        # 'sources': 'bbc-news', # can't use with country and category
        'category': category,  # business entertainment general health science sports technology
        'pageSize': 15,  # 20 is the default, 100 is the maximum.
        'page': page
    }
    if query:
        params_newsapi['q'] = query

    url_newsapi = 'https://newsapi.org/v2/top-headlines'
    try:
        response_news = requests.get(url=url_newsapi, params=params_newsapi)

        if response_news.json()['status'] == 'error':
            raise ex.ResponseStatusNewsAPIError(response_news.json()['code'], response_news.json()['message'])

        if not response_news:
            raise ex.ResponseStatusError(response_news.status_code)

        data_new = response_news.json()
        # with open('weather-5.json', 'w') as file:
        #         dump(data_news, file, indent=4, ensure_ascii=False)
        return data_new

    except (requests.RequestException, JSONDecodeError, ex.ResponseStatusError, ex.ResponseStatusNewsAPIError) as e:
        logger.exception(f'NewsError: {str(e)}')
        return None


async def news_dict(user_id: int,
                    first_name: str,
                    country: str = 'ru',
                    category: str = 'general',
                    query: Optional[str] = None) -> dict[int | None, list[float | str | None]] | str:
    """Return dictionary of news."""
    data_news = get_news(country=country, category=category, query=query)
    if not data_news:
        logger.warning(f'NewsError. User {first_name} (id:{user_id})')
        await database.add_request_db(user_id=user_id, type_request='news', num_tokens=0, status_request=False)
        return 'Error: can\'t get news'

    _news = {}
    for i in range(len(data_news['articles'])):
        _news[i] = [datetime.datetime.fromisoformat(data_news['articles'][i]['publishedAt']).strftime('%Y-%m-%d %H:%M'),
                    data_news['articles'][i]['author'],
                    data_news['articles'][i]['title'],
                    data_news['articles'][i]['description'],
                    data_news['articles'][i]['url']]
    await database.add_request_db(user_id=user_id, type_request='news', num_tokens=0, status_request=True)
    logger.info(
        f'Exit from news model user {first_name} (id:{user_id})')

    return _news


if __name__ == '__main__':
    news_dict_test = asyncio.run(news_dict(user_id=111, first_name='test', country='ru', category='general'))
    if isinstance(news_dict_test, str):
        print(news_dict_test)
    else:
        for key, value in news_dict_test.items():
            print(f'\n'.join([f'    {i}' for i in value if i is not None]) + '\n')
