import asyncio
import aiohttp
import admin.exeptions as ex
from admin.logsetting import logger
from create import TOKEN_OPENWEATHER
from json import JSONDecodeError
from databases import database
from typing import Optional, Any


def get_excluded(period: str) -> str:
    """Return string of excluded data."""
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
    """Get weather from OpenWeatherMap API."""
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
    """Parse weather from JSON-file and return dict."""
    # Import necessary modules for parsing weather
    if lang == 'ru':
        from util.weatherparse_ru import parse_weather, parse_minutely, parse_alerts
    else:
        from util.weatherparse_en import parse_weather, parse_minutely, parse_alerts

    exclude = get_excluded(period)

    show_long = True if volume == 'long' else False

    data_weather = await get_weather(lat=lat, lon=lon, lang=lang, exclude=exclude)

    if not data_weather:
        logger.warning(f'WeatherError. User {first_name} (id:{user_id})')
        await database.add_request_db(user_id=user_id, type_request='weather', num_tokens=0, status_request=False)
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

    await database.add_request_db(user_id=user_id, type_request='weather', num_tokens=0, status_request=True)
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
