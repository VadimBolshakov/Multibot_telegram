"""Get news via API https://newsapi.org/v2/top-headlines
    Return dist news values.
"""
import asyncio
import datetime
from json import JSONDecodeError
from typing import Optional

import aiohttp

from admin import exeptions as ex
from create import TOKEN_NEWSAPI, db, logger


async def get_news(country: str = '',
                   sources: str = 'bbc-news',
                   category: str = 'general',
                   query: Optional[str] = None,
                   page: int = 1) -> Optional[dict[str, str | int | float | list[dict[str, str | None]]]]:
    """Get news from NewsAPI API.

    :param country: country code, defaults to ''
    :type country: str, optional
    :param sources: sources, can't use with country and category, defaults to 'bbc-news'
    :type sources: str, optional
    :param category: category such as business, entertainment, general, health, science, sports and technology,
            defaults to 'general'
    :type category: str, optional
    :param query: query, defaults to None
    :type query: Optional[str], optional
    :param page: page, 20 is the default, 100 is the maximum, defaults to 1
    :type page: int, optional

    :raises aiohttp.ClientConnectorError: if connection error
    :raises ex.ResponseStatusError: is response status not 200
    :raises JSONDecodeError: if response not json
    :raises ex.ResponseStatusNewsAPIError: if response status error from NewsAPI
    :raises ex.ResponseTotalResultsNewsAPIError: if totalResults == 0

    :return: news
    :rtype: Optional[dict[str, str | int | float | list[dict[str, str | None]]]]
    """
    params_newsapi = {
        'apiKey': TOKEN_NEWSAPI,
        'country': country,
        # 'sources': 'bbc-news',
        'category': category,
        'pageSize': 15,
        'page': page
    }
    if query:
        params_newsapi['q'] = query

    url_newsapi = 'https://newsapi.org/v2/top-headlines'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url_newsapi, params=params_newsapi) as response:

                if response.status != 200:
                    raise ex.ResponseStatusError(response.status)

                data_newsapi = await response.json()

                if data_newsapi['status'] == 'error':
                    raise ex.ResponseStatusNewsAPIError(data_newsapi['code'], data_newsapi['message'])

                if data_newsapi['totalResults'] == 0:
                    raise ex.ResponseTotalResultsNewsAPIError()

                return data_newsapi

    except (aiohttp.ClientConnectorError, JSONDecodeError, ex.ResponseStatusError,
            ex.ResponseStatusNewsAPIError, ex.ResponseTotalResultsNewsAPIError) as e:
        logger.exception(f'NewsError: {str(e)}')
        return None


async def news_dict(user_id: int,
                    first_name: str,
                    country: str = '',
                    category: str = 'general',
                    query: Optional[str] = None) -> dict[int | None, list[float | str | None]] | str:
    """Return dictionary of news or error str if news data is None.

    :param user_id: user id
    :type user_id: int
    :param first_name: user first name
    :type first_name: str
    :param country: country code, defaults to ''
    :type country: str, optional
    :param category: category such as business, entertainment, general, health, science, sports and technology,
            defaults to 'general'
    :type category: str, optional
    :param query: query, defaults to None
    :type query: Optional[str], optional

    :return: dictionary of news
    :rtype: dict[int | None, list[float | str | None]] | str
    """
    data_news = await get_news(country=country, category=category, query=query)
    if not data_news:
        logger.warning(f'NewsError. User {first_name} (id:{user_id})')
        await db.add_request_db(user_id=user_id, type_request='news', num_tokens=0, status_request=False)
        return 'Error: can\'t get news'

    _news = {}
    for i in range(len(data_news['articles'])):
        _news[i] = [datetime.datetime.fromisoformat(data_news['articles'][i]['publishedAt']).strftime('%Y-%m-%d %H:%M'),
                    data_news['articles'][i]['author'],
                    data_news['articles'][i]['title'],
                    data_news['articles'][i]['description'],
                    data_news['articles'][i]['url']]
    await db.add_request_db(user_id=user_id, type_request='news', num_tokens=0, status_request=True)
    logger.info(
        f'Exit from news model user {first_name} (id:{user_id})')

    return _news


if __name__ == '__main__':
    news_dict_test = asyncio.run(news_dict(user_id=111, first_name='test', country='ru', category='general'))
    if isinstance(news_dict_test, str):
        print(news_dict_test)
    else:
        for key, value in news_dict_test.items():
            print('\n'.join([f'    {i}' for i in value if i is not None]) + '\n')
