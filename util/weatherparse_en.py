"""Weather parser for OpenWeatherMap API. English version."""
from datetime import datetime


def _moon_phase(moon_phase: float) -> str:
    """Return moon phase."""

    if moon_phase == 0:
        return 'New Moon'
    elif 0 < moon_phase < 0.25:
        return 'Waxing Crescent'
    elif moon_phase == 0.25:
        return 'First Quarter'
    elif 0.25 < moon_phase < 0.5:
        return 'Waxing Gibbous'
    elif moon_phase == 0.5:
        return 'Full Moon'
    elif 0.5 < moon_phase < 0.75:
        return 'Waning Gibbous'
    elif moon_phase == 0.75:
        return 'Last Quarter'
    elif 0.75 < moon_phase < 1:
        return 'Waning Crescent'
    elif moon_phase == 1:
        return 'New Moon'
    else:
        return 'Unknown'


wind_direction = {
    0: 'North',
    22.5: 'North-Northeast',
    45: 'Northeast',
    67.5: 'East-Northeast',
    90: 'East',
    112.5: 'East-Southeast',
    135: 'Southeast',
    157.5: 'South-Southeast',
    180: 'South',
    202.5: 'South-Southwest',
    225: 'Southwest',
    247.5: 'West-Southwest',
    270: 'West',
    292.5: 'West-Northwest',
    315: 'Northwest',
    337.5: 'North-Northwest',
    360: 'North'
}


def parse_weather(element: dict, timezone_offset: int, show_long: bool = True) -> list[str]:
    """Parse daily weather from JSON-file and return list.

    :param element: Element from JSON-file.
    :type element: dict
    :param timezone_offset: Timezone offset.
    :type timezone_offset: int
    :param show_long: Show long weather. Defaults to True.
    :type show_long: bool, optional

    :return: List with weather.
    :rtype: list[str]
    """
    weather = []
    if element.get('dt'):
        daily_dt = datetime.utcfromtimestamp(element['dt'] + timezone_offset).strftime('%Y-%m-%d %H:%M')
        weather.append(f'Weather on {daily_dt}')
    if element.get('sunrise') and show_long:
        sunrise = datetime.utcfromtimestamp(element['sunrise'] + timezone_offset).strftime('%H:%M')
        weather.append(f'Sunrise: {sunrise}')
    if element.get('sunset') and show_long:
        sunset = datetime.utcfromtimestamp(element['sunset'] + timezone_offset).strftime('%H:%M')
        weather.append(f'Sunset: {sunset}')
    if element.get('moonrise') and show_long:
        moonrise = datetime.utcfromtimestamp(element['moonrise'] + timezone_offset).strftime('%H:%M')
        weather.append(f'Moonrise: {moonrise}')
    if element.get('moonset') and show_long:
        moonset = datetime.utcfromtimestamp(element['moonset'] + timezone_offset).strftime('%H:%M')
        weather.append(f'Moonset: {moonset}')
    if element.get('moon_phase') and show_long:
        moon_phase = element['moon_phase']
        weather.append(f'Moon phase: {_moon_phase(moon_phase)}')
    if element.get('summary'):
        summary = element['summary']
        weather.append(f'Summary: {summary}')

    if element.get('weather'):
        if 'id' in element['weather'][0]:
            weather_id = element['weather'][0]['id']
        if ('main' in element['weather'][0]) and ('description' in element['weather'][0]) and show_long:
            weather_main = element['weather'][0]['main']
            weather_description = element['weather'][0]['description']
            weather.append(f'Weather : {weather_main}. {weather_description}')
        # if 'icon' in element['weather'][0]:
        #     weather_icon = element['weather'][0]['icon']
        #     weather.append(f'Weather_icon: {weather_icon}')

    if isinstance(element.get('temp'), dict):
        if element['temp'].get('morn') and show_long:
            temp_morn = element['temp']['morn']
            weather.append(f'Temperature morning: {round(temp_morn)}\u2103')
        if element['temp'].get('day'):
            temp_day = element['temp']['day']
            weather.append(f'Temperature day: {round(temp_day)}\u2103')
        if element['temp'].get('min'):
            temp_min = element['temp']['min']
            weather.append(f'Temperature min: {round(temp_min)}\u2103')
        if element['temp'].get('max'):
            temp_max = element['temp']['max']
            weather.append(f'Temperature max: {round(temp_max)}\u2103')
        if element['temp'].get('eve') and show_long:
            temp_eve = element['temp']['eve']
            weather.append(f'Temperature evening: {round(temp_eve)}\u2103')
        if element['temp'].get('night'):
            temp_night = element['temp']['night']
            weather.append(f'Temperature night: {round(temp_night)}\u2103')
    else:
        temp = element['temp']
        weather.append(f'Temperature: {round(temp)}\u2103')

    if isinstance(element.get('feels_like'), dict):
        if element['feels_like'].get('morn') and show_long:
            feels_like_morn = element['feels_like']['morn']
            weather.append(f'Feels like morning: {round(feels_like_morn)}\u2103')
        if element['feels_like'].get('day'):
            feels_like_day = element['feels_like']['day']
            weather.append(f'Feels like day: {round(feels_like_day)}\u2103')
        if element['feels_like'].get('eve') and show_long:
            feels_like_eve = element['feels_like']['eve']
            weather.append(f'Feels like evening: {round(feels_like_eve)}\u2103')
        if element['feels_like'].get('night'):
            feels_like_night = element['feels_like']['night']
            weather.append(f'Feels like night: {round(feels_like_night)}\u2103')
    else:
        feels_like = element['feels_like']
        weather.append(f'Feels like: {round(feels_like)}\u2103')

    if element.get('pressure'):
        pressure = element['pressure']
        weather.append(f'Pressure: {round(pressure * 0.75)} mmHg')
    if element.get('humidity'):
        humidity = element['humidity']
        weather.append(f'Humidity: {humidity}%')
    if element.get('dew_point') and show_long:
        dew_point = element['dew_point']
        weather.append(f'Dew point: {round(dew_point)}\u2103')
    if element.get('wind_speed'):
        wind_speed = element['wind_speed']
        weather.append(f'Wind speed: {wind_speed} m/s')
    if element.get('wind_deg'):
        wind_deg = element['wind_deg']
        weather.append(f'Wind direction: {wind_deg}° {wind_direction.get(round(wind_deg / 22.5) * 22.5)}')
    if element.get('wind_gust'):
        wind_gust = element['wind_gust']
        weather.append(f'Wind gust: {wind_gust} m/s')
    if element.get('clouds'):
        clouds = element['clouds']
        weather.append(f'Clouds: {clouds}%')
    if element.get('pop'):
        pop = element['pop']
        weather.append(f'Chance of precipitation: {round(pop * 100)}%')
    if element.get('rain'):
        if isinstance(element['rain'], dict):
            rain_1h = element['rain']['1h']
            weather.append(f'Rain: {rain_1h} mm/h')
        else:
            rain = element['rain']
            weather.append(f'Rain: {rain} mm')
    if element.get('snow'):
        if isinstance(element['snow'], dict):
            snow = element['snow']['1h']
            weather.append(f'Snow: {snow} mm/h')
        else:
            snow = element['snow']
            weather.append(f'Snow: {snow} mm')
    if element.get('uvi') and show_long:
        uvi = element['uvi']
        weather.append(f'UV index: {uvi}')
    if element.get('visibility'):
        visibility = element['visibility']
        weather.append(f'Visibility: {visibility} m')

    return weather


def parse_minutely(minutely_element: dict, timezone_offset: int, show_long: bool = True) -> list[str] | None:
    if minutely_element is None:
        return None
    minutely = []
    if ('dt' in minutely_element) & ('precipitation' in minutely_element):
        minutely_dt = datetime.utcfromtimestamp(minutely_element['dt'] + timezone_offset).strftime('%H:%M')
        minutely_precipitation = minutely_element['precipitation']
        if minutely_precipitation > 0:
            minutely.append(f'Time: {minutely_dt} precipitation: {minutely_precipitation} mm/h')

    return minutely


def parse_alerts(alerts_element: dict, timezone_offset: int, show_long: bool = True) -> list[str] | None:
    if alerts_element is None:
        return None
    alerts = []
    if ('sender_name' in alerts_element) & ('event' in alerts_element):
        alerts_sender_name = alerts_element['sender_name']
        alerts_event = alerts_element['event']
        alerts_start = datetime.utcfromtimestamp(alerts_element['start'] + timezone_offset).strftime('%Y-%m-%d %H:%M')
        alerts_end = datetime.utcfromtimestamp(alerts_element['end'] + timezone_offset).strftime('%Y-%m-%d %H:%M')
        alerts_description = alerts_element['description']
        alerts.append(f'{alerts_description}. '
                      f'According to the {alerts_sender_name} from {alerts_start} to {alerts_end} {alerts_event} is expected.')
    if 'tags' in alerts_element:
        alerts_tags = alerts_element['tags']

    return alerts


if __name__ == '__main__':
    pass
