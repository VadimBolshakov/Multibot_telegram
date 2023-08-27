"""This module is designed to get weather from OpenWeatherMap API via https://api.openweathermap.org/data/3.0/onecall?.
"""
import asyncio
from json import JSONDecodeError
from typing import Optional, Any

import aiohttp

import admin.exeptions as ex
from create import TOKEN_OPENWEATHER, db, logger


def get_excluded(period: str = '') -> str:
    """Return string of excluded data.

    :param period: period of weather, defaults to ''
    :type period: str, optional

    :return: string of excluded data
    :rtype: str
    """
    exclude = ''
    if period == 'current':
        exclude = 'hourly,daily'
    elif period == 'minutely':
        exclude = 'hourly,daily,alerts'
    elif period == 'hourly':
        exclude = 'daily'
    elif period == 'daily':
        exclude = 'minutely,hourly,alerts'
    return exclude


async def get_weather(lat: float,
                      lon: float,
                      units: str = 'metric',
                      lang: str = 'en',
                      exclude: str = '',
                      appid: str = TOKEN_OPENWEATHER) -> Optional[dict[str, Any]]:
    """Get weather from OpenWeatherMap API.

    :param lat: latitude
    :type lat: float
    :param lon: longitude
    :type lon: float
    :param units: units of measurement, defaults to 'metric'
    :type units: str, optional
    :param lang: language, defaults to 'en'
    :type lang: str, optional
    :param exclude: exclude data, defaults to ''
    :type exclude: str, optional
    :param appid: token for openweathermap, defaults to TOKEN_OPENWEATHER
    :type appid: str, optional

    :raises ex.ResponseStatusError: if response status not 200
    :raises JSONDecodeError: if response not json
    :raises aiohttp.ClientConnectorError: if connection error

    :return: weather
    :rtype: Optional[dict[str, Any]]
    """
    params_weather = {
        'lat': lat,
        'lon': lon,
        'units': units,
        'lang': lang,
        # 'exclude': 'minutely, hourly',
        'appid': appid
    }

    if exclude:
        params_weather['exclude'] = exclude

    url_weather = 'https://api.openweathermap.org/data/3.0/onecall?'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url_weather, params=params_weather) as response:
                if response.status != 200:
                    raise ex.ResponseStatusError(response.status)

                data_weather = await response.json()

                return data_weather

    except (aiohttp.ClientConnectorError, JSONDecodeError, ex.ResponseStatusError) as e:
        logger.exception(f'WeatherError: {str(e)}')
        return None


async def weather_dict(user_id: int,
                       first_name: str,
                       lat: float = 55.7522,
                       lon: float = 37.6156,
                       lang: str = 'en',
                       period: str = '',
                       volume: str = 'short') -> dict[str, list] | str:
    """Parse weather from JSON-file and return dict of the weather data or str if weather dataa is None.

    :param user_id: user id
    :type user_id: int
    :param first_name: user first name
    :type first_name: str
    :param lat: latitude, defaults to 55.7522
    :type lat: float, optional
    :param lon: longitude, defaults to 37.6156
    :type lon: float, optional
    :param lang: language, defaults to 'en'
    :type lang: str, optional
    :param period: period of weather, defaults to ''
    :type period: str, optional
    :param volume: volume of weather, defaults to 'short'
    :type volume: str, optional

    :return: weather
    :rtype: dict[str, list] | str
    """
    # Import necessary modules for parsing weather
    if lang == 'ru':
        from util.weatherparse_ru import parse_weather, parse_minutely, parse_alerts
    else:
        from util.weatherparse_en import parse_weather, parse_minutely, parse_alerts

    exclude = get_excluded(period)

    show_long = True if volume == 'full' else False

    data_weather = await get_weather(lat=lat, lon=lon, lang=lang, exclude=exclude)

    if not data_weather:
        logger.warning(f'WeatherError. User {first_name} (id:{user_id})')
        await db.add_request_db(user_id=user_id, type_request='weather', num_tokens=0, status_request=False)
        return 'Sorry, but we have not information about actual weather.'

    weather: dict[str, list] = {}

    time_zone = data_weather['timezone']
    timezone_offset = data_weather['timezone_offset']

    weather['timezone'] = [time_zone]

    if data_weather.get('current'):
        weather['current'] = parse_weather(data_weather['current'], timezone_offset, show_long)

    if data_weather.get('minutely'):
        weather['minutely'] = []
        for minutely_values in data_weather['minutely']:
            weather['minutely'].append(parse_minutely(minutely_values, timezone_offset, show_long))

    if data_weather.get('hourly'):
        weather['hourly'] = []
        for hourly_values in data_weather['hourly']:
            weather['hourly'].append(parse_weather(hourly_values, timezone_offset, show_long))

    if data_weather.get('daily'):
        weather['daily'] = []
        for daily_values in data_weather['daily']:
            weather['daily'].append(parse_weather(daily_values, timezone_offset, show_long))

    if 'alerts' in data_weather:
        weather['alerts'] = []
        for alerts_values in data_weather['alerts']:
            weather['alerts'].append(parse_alerts(alerts_values, timezone_offset, show_long))

    await db.add_request_db(user_id=user_id, type_request='weather', num_tokens=0, status_request=True)
    logger.info(
        f'Exit from weather model user {first_name} (id:{user_id})')

    return weather


if __name__ == '__main__':
    weather_test = asyncio.run(weather_dict(user_id=10, first_name='test', volume='long'))
    # print(weather_dict['minutely'])
    # print(weather_dict['hourly'])
    for key, value in weather_test.items():
        if isinstance(value[0], list):
            if key not in ('minutely', 'alerts'):
                [item.append('') for item in value]
            print(f'{key}:')
            print(f'\n'.join([f' {item}' for sublist in value for item in sublist if item is not None]))
        else:
            print(f'{key}:')
            print(f'\n'.join([f' {item}' for item in value if item is not None]))
