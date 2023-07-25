import requests
import admin.exeptions as ex
from admin.logsetting import logger
from create import TOKEN_OPENWEATHER
from json import JSONDecodeError
from typing import Optional
from util.weatherparse_ru import parse_daily, parse_hourly, parse_current, parse_alerts, parse_minutely
from databases import database


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


def get_weather(lat: float,
                lon: float,
                units: str = 'metric',
                lang: str = 'en',
                exclude: str = '',
                appid: str = TOKEN_OPENWEATHER) -> Optional[dict[str, str | int | float | list | dict]]:
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
        response_weather = requests.get(url=url_weather, params=params_weather)

        if not response_weather:
            raise ex.ResponseStatusError(response_weather.status_code)

        data_weather = response_weather.json()
        # with open('weather-4.json', 'w') as file:
        #         dump(data_weather, file, indent=4, ensure_ascii=False)
        return data_weather

    except (requests.RequestException, JSONDecodeError, ex.ResponseStatusError) as e:
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
    exclude = get_excluded(period)

    show_long = True if volume == 'long' else False

    data_weather = get_weather(lat=lat, lon=lon, lang=lang, exclude=exclude)

    if not data_weather:
        logger.warning(f'WeatherError. User {first_name} (id:{user_id})')
        await database.add_request_db(user_id=user_id, type_request='weather', num_tokens=0, status_request=False)
        return 'Sorry, but we have not information about actual weather.'

    weather: dict[str, list] = {}

    time_zone = data_weather['timezone']
    timezone_offset = data_weather['timezone_offset']

    weather['timezone'] = [time_zone]

    if 'current' in data_weather:
        weather['current'] = parse_current(data_weather['current'], timezone_offset, show_long)

    if 'minutely' in data_weather:
        weather['minutely'] = []
        for minutely_values in data_weather['minutely']:
            weather['minutely'].append(parse_minutely(minutely_values, timezone_offset, show_long))

    if 'hourly' in data_weather:
        weather['hourly'] = []
        for hourly_values in data_weather['hourly']:
            weather['hourly'].append(parse_hourly(hourly_values, timezone_offset, show_long))

    if 'daily' in data_weather:
        weather['daily'] = []
        for daily_values in data_weather['daily']:
            weather['daily'].append(parse_daily(daily_values, timezone_offset, show_long))

    if 'alerts' in data_weather:
        weather['alerts'] = []
        for alerts_values in data_weather['alerts']:
            weather['alerts'].append(parse_alerts(alerts_values, timezone_offset, show_long))

    await database.add_request_db(user_id=user_id, type_request='weather', num_tokens=0, status_request=True)
    logger.info(
        f'Exit from weather model user {first_name} (id:{user_id})')

    return weather


if __name__ == '__main__':
    weather_test = await weather_dict(user_id=10, first_name='test', volume='long')
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
