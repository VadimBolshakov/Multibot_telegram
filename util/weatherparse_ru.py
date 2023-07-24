from datetime import datetime


def _moon_phase(moon_phase: float) -> str:
    """Return moon phase."""
    if moon_phase == 0:
        return 'Новолуние'
    elif 0 < moon_phase < 0.25:
        return 'Растущий месяц'
    elif moon_phase == 0.25:
        return 'Первая четверть'
    elif 0.25 < moon_phase < 0.5:
        return 'Растущий гиббус'
    elif moon_phase == 0.5:
        return 'Полнолуние'
    elif 0.5 < moon_phase < 0.75:
        return 'Убывающий месяц'
    elif moon_phase == 0.75:
        return 'Последняя четверть'
    elif 0.75 < moon_phase < 1:
        return 'Убывающий гиббус'
    elif moon_phase == 1:
        return 'Новолуние'
    else:
        return 'Unknown'


wind_direction = {
    0: 'North',
    22.5: 'Северо-северо-восток',
    45: 'Северо-восток',
    67.5: 'Восток-северо-восток',
    90: 'Восток',
    112.5: 'Восток-юго-восток',
    135: 'Юго-восток',
    157.5: 'Юго-юго-восток',
    180: 'Юг',
    202.5: 'Юго-юго-запад',
    225: 'Юго-запад',
    247.5: 'Запад-юго-запад',
    270: 'Запад',
    292.5: 'Запад-северо-запад',
    315: 'Северо-запад',
    337.5: 'Северо-северо-запад',
    360: 'Север'
}


def parse_daily(daily_element: dict, timezone_offset: int, show_long: bool = True) -> list[str]:
    """Parse daily weather from JSON-file and return list."""
    daily = []
    if 'dt' in daily_element:
        daily_dt = datetime.utcfromtimestamp(daily_element['dt'] + timezone_offset).strftime('%Y-%m-%d')
        daily.append(f'Погода на {daily_dt}')
    if ('sunrise' in daily_element) & show_long:
        daily_sunrise = datetime.utcfromtimestamp(daily_element['sunrise'] + timezone_offset).strftime('%H:%M')
        daily.append(f'Расвет: {daily_sunrise}')
    if ('sunset' in daily_element) & show_long:
        daily_sunset = datetime.utcfromtimestamp(daily_element['sunset'] + timezone_offset).strftime('%H:%M')
        daily.append(f'Закат: {daily_sunset}')
    if ('moonrise' in daily_element) & show_long:
        daily_moonrise = datetime.utcfromtimestamp(daily_element['moonrise'] + timezone_offset).strftime('%H:%M')
        daily.append(f'Восход луны: {daily_moonrise}')
    if ('moonset' in daily_element) & show_long:
        daily_moonset = datetime.utcfromtimestamp(daily_element['moonset'] + timezone_offset).strftime('%H:%M')
        daily.append(f'Заход луны: {daily_moonset}')
    if ('moon_phase' in daily_element) & show_long:
        daily_moon_phase = daily_element['moon_phase']
        daily.append(f'Фаза луны: {_moon_phase(daily_moon_phase)}')
    if 'summary' in daily_element:
        daily_summary = daily_element['summary']
        daily.append(f'Общее: {daily_summary}')

    if 'temp' in daily_element:
        if ('morn' in daily_element['temp']) & show_long:
            daily_temp_morn = daily_element['temp']['morn']
            daily.append(f'Температра утром: {round(daily_temp_morn)}\u2103')
        if 'day' in daily_element['temp']:
            daily_temp_day = daily_element['temp']['day']
            daily.append(f'Температра днем: {round(daily_temp_day)}\u2103')
        if 'min' in daily_element['temp']:
            daily_temp_min = daily_element['temp']['min']
            daily.append(f'Температра min: {round(daily_temp_min)}\u2103')
        if 'max' in daily_element['temp']:
            daily_temp_max = daily_element['temp']['max']
            daily.append(f'Температра max: {round(daily_temp_max)}\u2103')
        if ('eve' in daily_element['temp']) & show_long:
            daily_temp_eve = daily_element['temp']['eve']
            daily.append(f'Температра вечером: {round(daily_temp_eve)}\u2103')
        if 'night' in daily_element['temp']:
            daily_temp_night = daily_element['temp']['night']
            daily.append(f'Температра ночью: {round(daily_temp_night)}\u2103')

    if 'feels_like' in daily_element:
        if ('morn' in daily_element['feels_like']) & show_long:
            daily_feels_like_morn = daily_element['feels_like']['morn']
            daily.append(f'Ощущается утром как : {round(daily_feels_like_morn)}\u2103')
        if 'day' in daily_element['feels_like']:
            daily_feels_like_day = daily_element['feels_like']['day']
            daily.append(f'Ощущается днем как : {round(daily_feels_like_day)}\u2103')
        if 'night' in daily_element['feels_like']:
            daily_feels_like_night = daily_element['feels_like']['night']
            daily.append(f'Ощущается ночью как : {round(daily_feels_like_night)}\u2103')
        if ('eve' in daily_element['feels_like']) & show_long:
            daily_feels_like_eve = daily_element['feels_like']['eve']
            daily.append(f'Ощущается вечером как : {round(daily_feels_like_eve)}\u2103')

    if 'pressure' in daily_element:
        daily_pressure = daily_element['pressure']
        daily.append(f'Давление: {round(daily_pressure * 0.75)} mmHg')
    if 'humidity' in daily_element:
        daily_humidity = daily_element['humidity']
        daily.append(f'Влажность: {daily_humidity} %')
    if 'dew_point' in daily_element:
        daily_dew_point = daily_element['dew_point']
        daily.append(f'Точка росы: {round(daily_dew_point)}\u2103')
    if 'wind_speed' in daily_element:
        daily_wind_speed = daily_element['wind_speed']
        daily.append(f'Скорость ветра: {daily_wind_speed} m/s')
    if 'wind_deg' in daily_element:
        daily_wind_deg = daily_element['wind_deg']
        daily.append(f'Напрвление ветра: {wind_direction.get(round(daily_wind_deg / 22.5) * 22.5)}')
    if 'wind_gust' in daily_element:
        daily_wind_gust = daily_element['wind_gust']
        daily.append(f'Порывы ветра: {daily_wind_gust} m/s')
    if 'clouds' in daily_element:
        daily_clouds = daily_element['clouds']
        daily.append(f'Облачность: {daily_clouds} %')
    if 'pop' in daily_element:
        daily_pop = daily_element['pop']
        daily.append(f'Вероятность осадков: {daily_pop}')
    if 'rain' in daily_element:
        daily_rain = daily_element['rain']
        daily.append(f'Дождь: {daily_rain} mm')
    if 'uvi' in daily_element:
        daily_uvi = daily_element['uvi']
        daily.append(f'Индекс УФ: {daily_uvi}')
    if 'snow' in daily_element:
        daily_snow = daily_element['snow']
        daily.append(f'Снег: {daily_snow} mm')
    if 'weather' in daily_element:
        if 'id' in daily_element['weather'][0]:
            daily_weather_id = daily_element['weather'][0]['id']
        if ('main' in daily_element['weather'][0]) & ('description' in daily_element['weather'][0]) & show_long:
            daily_weather_main = daily_element['weather'][0]['main']
            daily_weather_description = daily_element['weather'][0]['description']
            daily.append(f'Погода : {daily_weather_main}. {daily_weather_description}')
        if 'icon' in daily_element['weather'][0]:
            daily_weather_icon = daily_element['weather'][0]['icon']

    return daily


def parse_hourly(hourly_element: dict, timezone_offset: int, show_long: bool = True) -> list[str]:
    hourly = []

    if 'dt' in hourly_element:
        hourly_dt = datetime.utcfromtimestamp(hourly_element['dt'] + timezone_offset).strftime('%Y-%m-%d %H:%M')
        hourly.append(f'Дата и время: {hourly_dt}')
    if 'temp' in hourly_element:
        hourly_temp = hourly_element['temp']
        hourly.append(f'Температра: {round(hourly_temp)}\u2103')
    if 'feels_like' in hourly_element:
        hourly_feels_like = hourly_element['feels_like']
        hourly.append(f'Ощущается как: {round(hourly_feels_like)}\u2103')
    if 'pressure' in hourly_element:
        hourly_pressure = hourly_element['pressure']
        hourly.append(f'Давление: {round(hourly_pressure * 0.75)} mmHg')
    if 'humidity' in hourly_element:
        hourly_humidity = hourly_element['humidity']
        hourly.append(f'Влажность: {hourly_humidity} %')
    if ('dew_point' in hourly_element) & show_long:
        hourly_dew_point = hourly_element['dew_point']
        hourly.append(f'Точка росы: {round(hourly_dew_point)}\u2103')
    if ('uvi' in hourly_element) & show_long:
        hourly_uvi = hourly_element['uvi']
        hourly.append(f'Индекс УФ: {hourly_uvi}')
    if 'clouds' in hourly_element:
        hourly_clouds = hourly_element['clouds']
        hourly.append(f'Облачность: {hourly_clouds} %')
    if 'visibility' in hourly_element:
        hourly_visibility = hourly_element['visibility']
        hourly.append(f'Видимость: {hourly_visibility} m')
    if 'wind_speed' in hourly_element:
        hourly_wind_speed = hourly_element['wind_speed']
        hourly.append(f'Скорость верта: {hourly_wind_speed} m/s')
    if 'wind_deg' in hourly_element:
        hourly_wind_deg = hourly_element['wind_deg']
        hourly.append(f'Направление ветра: {wind_direction.get(round(hourly_wind_deg / 22.5) * 22.5)}')
    if 'wind_gust' in hourly_element:
        hourly_wind_gust = hourly_element['wind_gust']
        hourly.append(f'Порывы ветра: {hourly_wind_gust} m/s')
    if 'pop' in hourly_element:
        hourly_pop = hourly_element['pop']
        hourly.append(f'Вероятность осадков: {hourly_pop}')
    if 'rain' in hourly_element:
        hourly_rain = hourly_element['rain']
        hourly.append(f'Дождь: {hourly_rain} mm/h')
    if 'snow' in hourly_element:
        hourly_snow = hourly_element['snow']
        hourly.append(f'Снег: {hourly_snow} mm/h')
    if 'weather' in hourly_element:
        if 'id' in hourly_element['weather'][0]:
            hourly_weather_id = hourly_element['weather'][0]['id']
        if ('main' in hourly_element['weather'][0]) & ('description' in hourly_element['weather'][0]) & show_long:
            hourly_weather_main = hourly_element['weather'][0]['main']
            hourly_weather_description = hourly_element['weather'][0]['description']
            hourly.append(f'Погода : {hourly_weather_main}. {hourly_weather_description}')
        if 'icon' in hourly_element['weather'][0]:
            hourly_weather_icon = hourly_element['weather'][0]['icon']

    return hourly


def parse_current(current_element: dict, timezone_offset: int, show_long: bool = True) -> list[str]:
    current = []

    if 'dt' in current_element:
        current_dt = datetime.utcfromtimestamp(current_element['dt'] + timezone_offset).strftime('%Y-%m-%d %H:%M:%S')
        current.append(f'Текущее время: {current_dt}')
    if 'sunrise' in current_element:
        current_sunrise = datetime.utcfromtimestamp(current_element['sunrise'] + timezone_offset).strftime('%H:%M')
        current.append(f'Рассвет: {current_sunrise}')
    if 'sunset' in current_element:
        current_sunset = datetime.utcfromtimestamp(current_element['sunset'] + timezone_offset).strftime('%H:%M')
        current.append(f'Закат: {current_sunset}')
    if 'temp' in current_element:
        current_temp = current_element['temp']
        current.append(f'Температра: {round(current_temp)} \u2103')
    if 'feels_like' in current_element:
        current_feels_like = current_element['feels_like']
        current.append(f'Ощущается как: {round(current_feels_like)} \u2103')
    if 'pressure' in current_element:
        current_pressure = current_element['pressure']
        current.append(f'Давление: {round(current_pressure * 0.75)} mmHg')
    if 'humidity' in current_element:
        current_humidity = current_element['humidity']
        current.append(f'Влажность: {current_humidity}%')
    if 'dew_point' in current_element:
        current_dew_point = current_element['dew_point']
        current.append(f'Точка росы: {round(current_dew_point)} \u2103')
    if 'uvi' in current_element:
        current_uvi = current_element['uvi']
        current.append(f'Индекс УФ: {current_uvi}')
    if 'clouds' in current_element:
        current_clouds = current_element['clouds']
        current.append(f'Облачность: {current_clouds}%')
    if 'visibility' in current_element:
        current_visibility = current_element['visibility']
        current.append(f'Видимость: {current_visibility} m')
    if 'wind_speed' in current_element:
        current_wind_speed = current_element['wind_speed']
        current.append(f'Скорость ветра: {current_wind_speed} m/s')
    if 'wind_deg' in current_element:
        current_wind_deg = current_element['wind_deg']
        current.append(f'направление ветра: {wind_direction.get(round(current_wind_deg / 22.5) * 22.5)}')
    if 'wind_gust' in current_element:
        current_wind_gust = current_element['wind_gust']
        current.append(f'порывы ветра: {current_wind_gust} m/s')
    if 'rain' in current_element:
        current_rain = current_element['rain']['1h']
        current.append(f'Дождь: {current_rain} mm/h')
    if 'snow' in current_element:
        current_snow = current_element['snow']['1h']
        current.append(f'Снег: {current_snow} mm/h')
    if 'weather' in current_element:
        current_weather_id = current_element['weather'][0]['id']
        current_weather_main = current_element['weather'][0]['main']
        current_weather_description = current_element['weather'][0]['description']
        current_weather_icon = current_element['weather'][0]['icon']
        current.append(f'Погода: {current_weather_main}.  {current_weather_description}')

    return current


def parse_minutely(minutely_element: dict, timezone_offset: int, show_long: bool = True) -> list[str] | None:
    if minutely_element is None:
        return None
    minutely = []
    if ('dt' in minutely_element) & ('precipitation' in minutely_element):
        minutely_dt = datetime.utcfromtimestamp(minutely_element['dt'] + timezone_offset).strftime('%H:%M')
        minutely_precipitation = minutely_element['precipitation']
        if minutely_precipitation > 0:
            minutely.append(f'Время: {minutely_dt} осадки: {minutely_precipitation} mm/h')

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
        alerts.append(f'По информации {alerts_sender_name} с {alerts_start} до {alerts_end} ожидается {alerts_event}.{alerts_description}')
    if 'tags' in alerts_element:
        alerts_tags = alerts_element['tags']

    return alerts


if __name__ == '__main__':
    pass
