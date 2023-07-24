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


def parse_daily(daily_element: dict, timezone_offset: int, show_long: bool = True) -> list[str]:
    """Parse daily weather from JSON-file and return list."""
    daily = []
    if 'dt' in daily_element:
        daily_dt = datetime.utcfromtimestamp(daily_element['dt'] + timezone_offset).strftime('%Y-%m-%d')
        daily.append(f'Weather on {daily_dt}')
    if ('sunrise' in daily_element) & show_long:
        daily_sunrise = datetime.utcfromtimestamp(daily_element['sunrise'] + timezone_offset).strftime('%H:%M')
        daily.append(f'Sunrise: {daily_sunrise}')
    if ('sunset' in daily_element) & show_long:
        daily_sunset = datetime.utcfromtimestamp(daily_element['sunset'] + timezone_offset).strftime('%H:%M')
        daily.append(f'Sunset: {daily_sunset}')
    if ('moonrise' in daily_element) & show_long:
        daily_moonrise = datetime.utcfromtimestamp(daily_element['moonrise'] + timezone_offset).strftime('%H:%M')
        daily.append(f'Moonrise: {daily_moonrise}')
    if ('moonset' in daily_element) & show_long:
        daily_moonset = datetime.utcfromtimestamp(daily_element['moonset'] + timezone_offset).strftime('%H:%M')
        daily.append(f'Moonset: {daily_moonset}')
    if ('moon_phase' in daily_element) & show_long:
        daily_moon_phase = daily_element['moon_phase']
        daily.append(f'Moon phase: {_moon_phase(daily_moon_phase)}')
    if 'summary' in daily_element:
        daily_summary = daily_element['summary']
        daily.append(f'Summary: {daily_summary}')

    if 'temp' in daily_element:
        if ('morn' in daily_element['temp']) & show_long:
            daily_temp_morn = daily_element['temp']['morn']
            daily.append(f'Temperature morning: {round(daily_temp_morn)}\u2103')
        if 'day' in daily_element['temp']:
            daily_temp_day = daily_element['temp']['day']
            daily.append(f'Temperature day: {round(daily_temp_day)}\u2103')
        if 'min' in daily_element['temp']:
            daily_temp_min = daily_element['temp']['min']
            daily.append(f'Temperature min: {round(daily_temp_min)}\u2103')
        if 'max' in daily_element['temp']:
            daily_temp_max = daily_element['temp']['max']
            daily.append(f'Temperature max: {round(daily_temp_max)}\u2103')
        if ('eve' in daily_element['temp']) & show_long:
            daily_temp_eve = daily_element['temp']['eve']
            daily.append(f'Temperature evening: {round(daily_temp_eve)}\u2103')
        if 'night' in daily_element['temp']:
            daily_temp_night = daily_element['temp']['night']
            daily.append(f'Temperature night: {round(daily_temp_night)}\u2103')

    if 'feels_like' in daily_element:
        if ('morn' in daily_element['feels_like']) & show_long:
            daily_feels_like_morn = daily_element['feels_like']['morn']
            daily.append(f'Feels like morning: {round(daily_feels_like_morn)}\u2103')
        if 'day' in daily_element['feels_like']:
            daily_feels_like_day = daily_element['feels_like']['day']
            daily.append(f'Feels like day: {round(daily_feels_like_day)}\u2103')
        if 'night' in daily_element['feels_like']:
            daily_feels_like_night = daily_element['feels_like']['night']
            daily.append(f'Feels like night: {round(daily_feels_like_night)}\u2103')
        if ('eve' in daily_element['feels_like']) & show_long:
            daily_feels_like_eve = daily_element['feels_like']['eve']
            daily.append(f'Feels like evening: {round(daily_feels_like_eve)}\u2103')

    if 'pressure' in daily_element:
        daily_pressure = daily_element['pressure']
        daily.append(f'Pressure: {round(daily_pressure * 0.75)} mmHg')
    if 'humidity' in daily_element:
        daily_humidity = daily_element['humidity']
        daily.append(f'Humidity: {daily_humidity} %')
    if 'dew_point' in daily_element:
        daily_dew_point = daily_element['dew_point']
        daily.append(f'Dew point: {round(daily_dew_point)}\u2103')
    if 'wind_speed' in daily_element:
        daily_wind_speed = daily_element['wind_speed']
        daily.append(f'Wind speed: {daily_wind_speed} m/s')
    if 'wind_deg' in daily_element:
        daily_wind_deg = daily_element['wind_deg']
        daily.append(f'Wind direction: {wind_direction.get(round(daily_wind_deg / 22.5) * 22.5)}')
    if 'wind_gust' in daily_element:
        daily_wind_gust = daily_element['wind_gust']
        daily.append(f'Wind gust: {daily_wind_gust} m/s')
    if 'clouds' in daily_element:
        daily_clouds = daily_element['clouds']
        daily.append(f'Clouds: {daily_clouds} %')
    if 'pop' in daily_element:
        daily_pop = daily_element['pop']
        daily.append(f'Probability of precipitation: {daily_pop}')
    if 'rain' in daily_element:
        daily_rain = daily_element['rain']
        daily.append(f'Rain: {daily_rain} mm')
    if 'uvi' in daily_element:
        daily_uvi = daily_element['uvi']
        daily.append(f'UV index: {daily_uvi}')
    if 'snow' in daily_element:
        daily_snow = daily_element['snow']
        daily.append(f'Snow: {daily_snow} mm')
    if 'weather' in daily_element:
        if 'id' in daily_element['weather'][0]:
            daily_weather_id = daily_element['weather'][0]['id']
        if ('main' in daily_element['weather'][0]) & ('description' in daily_element['weather'][0]) & show_long:
            daily_weather_main = daily_element['weather'][0]['main']
            daily_weather_description = daily_element['weather'][0]['description']
            daily.append(f'Weather : {daily_weather_main}. {daily_weather_description}')
        if 'icon' in daily_element['weather'][0]:
            daily_weather_icon = daily_element['weather'][0]['icon']

    return daily


def parse_hourly(hourly_element: dict, timezone_offset: int, show_long: bool = True) -> list[str]:
    hourly = []

    if 'dt' in hourly_element:
        hourly_dt = datetime.utcfromtimestamp(hourly_element['dt'] + timezone_offset).strftime('%Y-%m-%d %H:%M')
        hourly.append(f'Date and time: {hourly_dt}')
    if 'temp' in hourly_element:
        hourly_temp = hourly_element['temp']
        hourly.append(f'Temperature: {round(hourly_temp)}\u2103')
    if 'feels_like' in hourly_element:
        hourly_feels_like = hourly_element['feels_like']
        hourly.append(f'Feels like: {round(hourly_feels_like)}\u2103')
    if 'pressure' in hourly_element:
        hourly_pressure = hourly_element['pressure']
        hourly.append(f'Pressure: {round(hourly_pressure * 0.75)} mmHg')
    if 'humidity' in hourly_element:
        hourly_humidity = hourly_element['humidity']
        hourly.append(f'Humidity: {hourly_humidity} %')
    if ('dew_point' in hourly_element) & show_long:
        hourly_dew_point = hourly_element['dew_point']
        hourly.append(f'Dew point: {round(hourly_dew_point)}\u2103')
    if ('uvi' in hourly_element) & show_long:
        hourly_uvi = hourly_element['uvi']
        hourly.append(f'UV index: {hourly_uvi}')
    if 'clouds' in hourly_element:
        hourly_clouds = hourly_element['clouds']
        hourly.append(f'Clouds: {hourly_clouds} %')
    if 'visibility' in hourly_element:
        hourly_visibility = hourly_element['visibility']
        hourly.append(f'Visibility: {hourly_visibility} m')
    if 'wind_speed' in hourly_element:
        hourly_wind_speed = hourly_element['wind_speed']
        hourly.append(f'Wind speed: {hourly_wind_speed} m/s')
    if 'wind_deg' in hourly_element:
        hourly_wind_deg = hourly_element['wind_deg']
        hourly.append(f'Wind direction: {wind_direction.get(round(hourly_wind_deg / 22.5) * 22.5)}')
    if 'wind_gust' in hourly_element:
        hourly_wind_gust = hourly_element['wind_gust']
        hourly.append(f'Wind gust: {hourly_wind_gust} m/s')
    if 'pop' in hourly_element:
        hourly_pop = hourly_element['pop']
        hourly.append(f'Probability of precipitation: {hourly_pop}')
    if 'rain' in hourly_element:
        hourly_rain = hourly_element['rain']
        hourly.append(f'Rain: {hourly_rain} mm/h')
    if 'snow' in hourly_element:
        hourly_snow = hourly_element['snow']
        hourly.append(f'Snow: {hourly_snow} mm/h')
    if 'weather' in hourly_element:
        if 'id' in hourly_element['weather'][0]:
            hourly_weather_id = hourly_element['weather'][0]['id']
        if ('main' in hourly_element['weather'][0]) & ('description' in hourly_element['weather'][0]) & show_long:
            hourly_weather_main = hourly_element['weather'][0]['main']
            hourly_weather_description = hourly_element['weather'][0]['description']
            hourly.append(f'Weather : {hourly_weather_main}. {hourly_weather_description}')
        if 'icon' in hourly_element['weather'][0]:
            hourly_weather_icon = hourly_element['weather'][0]['icon']

    return hourly


def parse_current(current_element: dict, timezone_offset: int, show_long: bool = True) -> list[str]:
    current = []

    if 'dt' in current_element:
        current_dt = datetime.utcfromtimestamp(current_element['dt'] + timezone_offset).strftime('%Y-%m-%d %H:%M:%S')
        current.append(f'Current time: {current_dt}')
    if 'sunrise' in current_element:
        current_sunrise = datetime.utcfromtimestamp(current_element['sunrise'] + timezone_offset).strftime('%H:%M')
        current.append(f'Sunrise: {current_sunrise}')
    if 'sunset' in current_element:
        current_sunset = datetime.utcfromtimestamp(current_element['sunset'] + timezone_offset).strftime('%H:%M')
        current.append(f'Sunset: {current_sunset}')
    if 'temp' in current_element:
        current_temp = current_element['temp']
        current.append(f'Temperature: {round(current_temp)} \u2103')
    if 'feels_like' in current_element:
        current_feels_like = current_element['feels_like']
        current.append(f'Feels like: {round(current_feels_like)} \u2103')
    if 'pressure' in current_element:
        current_pressure = current_element['pressure']
        current.append(f'Pressure: {round(current_pressure * 0.75)} mmHg')
    if 'humidity' in current_element:
        current_humidity = current_element['humidity']
        current.append(f'Humidity: {current_humidity}%')
    if 'dew_point' in current_element:
        current_dew_point = current_element['dew_point']
        current.append(f'Dew point: {round(current_dew_point)} \u2103')
    if 'uvi' in current_element:
        current_uvi = current_element['uvi']
        current.append(f'UV index: {current_uvi}')
    if 'clouds' in current_element:
        current_clouds = current_element['clouds']
        current.append(f'Clouds: {current_clouds}%')
    if 'visibility' in current_element:
        current_visibility = current_element['visibility']
        current.append(f'Visibility: {current_visibility} m')
    if 'wind_speed' in current_element:
        current_wind_speed = current_element['wind_speed']
        current.append(f'Wind speed: {current_wind_speed} m/s')
    if 'wind_deg' in current_element:
        current_wind_deg = current_element['wind_deg']
        current.append(f'Wind direction: {wind_direction.get(round(current_wind_deg / 22.5) * 22.5)}')
    if 'wind_gust' in current_element:
        current_wind_gust = current_element['wind_gust']
        current.append(f'Wind gust: {current_wind_gust} m/s')
    if 'rain' in current_element:
        current_rain = current_element['rain']['1h']
        current.append(f'Rain: {current_rain} mm/h')
    if 'snow' in current_element:
        current_snow = current_element['snow']['1h']
        current.append(f'Snow: {current_snow} mm/h')
    if 'weather' in current_element:
        current_weather_id = current_element['weather'][0]['id']
        current_weather_main = current_element['weather'][0]['main']
        current_weather_description = current_element['weather'][0]['description']
        current_weather_icon = current_element['weather'][0]['icon']
        current.append(f'Weather: {current_weather_main}.  {current_weather_description}')

    return current


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
        alerts.append(f'{alerts_description}. According to the {alerts_sender_name} from {alerts_start} to {alerts_end} {alerts_event} is expected.')
    if 'tags' in alerts_element:
        alerts_tags = alerts_element['tags']

    return alerts


if __name__ == '__main__':
    pass
