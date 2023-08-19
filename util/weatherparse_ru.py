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


def parse_weather(element: dict, timezone_offset: int, show_long: bool = True) -> list[str]:
    """Parse daily weather from JSON-file and return list."""
    weather = []
    if element.get('dt'):
        daily_dt = datetime.utcfromtimestamp(element['dt'] + timezone_offset).strftime('%Y-%m-%d %H:%M')
        weather.append(f'Погода на {daily_dt}')
    if element.get('sunrise') and show_long:
        sunrise = datetime.utcfromtimestamp(element['sunrise'] + timezone_offset).strftime('%H:%M')
        weather.append(f'Рассвет: {sunrise}')
    if element.get('sunset') and show_long:
        sunset = datetime.utcfromtimestamp(element['sunset'] + timezone_offset).strftime('%H:%M')
        weather.append(f'Закат: {sunset}')
    if element.get('moonrise') and show_long:
        moonrise = datetime.utcfromtimestamp(element['moonrise'] + timezone_offset).strftime('%H:%M')
        weather.append(f'Восход луны: {moonrise}')
    if element.get('moonset', False) and show_long:
        moonset = datetime.utcfromtimestamp(element['moonset'] + timezone_offset).strftime('%H:%M')
        weather.append(f'Заход луны: {moonset}')
    if element.get('moon_phase') and show_long:
        moon_phase = element['moon_phase']
        weather.append(f'Фаза луны: {_moon_phase(moon_phase)}')
    # if element.get('summary'):
    #     summary = element['summary']
    #     weather.append(f'Общее: {summary}')

    if element.get('weather'):
        if 'id' in element['weather'][0]:
            weather_id = element['weather'][0]['id']
        if ('main' in element['weather'][0]) and ('description' in element['weather'][0]) and show_long:
            weather_main = element['weather'][0]['main']
            weather_description = element['weather'][0]['description']
            weather.append(f'Погода : {weather_main}. {weather_description}')
        # if 'icon' in element['weather'][0]:
        #     weather_icon = element['weather'][0]['icon']
        #     weather.append(f'Weather_icon: {weather_icon}')

    if isinstance(element.get('temp'), dict):
        if element['temp'].get('morn') and show_long:
            temp_morn = element['temp']['morn']
            weather.append(f'Температура утром: {round(temp_morn)}\u2103')
        if element['temp'].get('day'):
            temp_day = element['temp']['day']
            weather.append(f'Температура днём: {round(temp_day)}\u2103')
        if element['temp'].get('min'):
            temp_min = element['temp']['min']
            weather.append(f'Температура min: {round(temp_min)}\u2103')
        if element['temp'].get('max'):
            temp_max = element['temp']['max']
            weather.append(f'Температура max: {round(temp_max)}\u2103')
        if element['temp'].get('eve') and show_long:
            temp_eve = element['temp']['eve']
            weather.append(f'Температура вечером: {round(temp_eve)}\u2103')
        if element['temp'].get('night'):
            temp_night = element['temp']['night']
            weather.append(f'Температура ночью: {round(temp_night)}\u2103')
    else:
        temp = element['temp']
        weather.append(f'Температура: {round(temp)}\u2103')

    if isinstance(element.get('feels_like'), dict):
        if element['feels_like'].get('morn', False) and show_long:
            feels_like_morn = element['feels_like']['morn']
            weather.append(f'Ощущается как утром: {round(feels_like_morn)}\u2103')
        if element['feels_like'].get('day'):
            feels_like_day = element['feels_like']['day']
            weather.append(f'Ощущается как днём: {round(feels_like_day)}\u2103')
        if element['feels_like'].get('eve') and  show_long:
            feels_like_eve = element['feels_like']['eve']
            weather.append(f'Ощущается как вечером: {round(feels_like_eve)}\u2103')
        if element['feels_like'].get('night'):
            feels_like_night = element['feels_like']['night']
            weather.append(f'Ощущается как ночью: {round(feels_like_night)}\u2103')
    else:
        feels_like = element['feels_like']
        weather.append(f'Ощущается как: {round(feels_like)}\u2103')

    if element.get('pressure'):
        pressure = element['pressure']
        weather.append(f'Давление: {round(pressure * 0.75)} мм. рт. ст.')
    if element.get('humidity'):
        humidity = element['humidity']
        weather.append(f'Влажность: {humidity}%')
    if element.get('dew_point') and show_long:
        dew_point = element['dew_point']
        weather.append(f'Точка росы: {round(dew_point)}\u2103')
    if element.get('wind_speed'):
        wind_speed = element['wind_speed']
        weather.append(f'Скорость ветра: {wind_speed} м/с')
    if element.get('wind_deg'):
        wind_deg = element['wind_deg']
        weather.append(f'Направление ветра: {wind_deg}° {wind_direction.get(round(wind_deg / 22.5) * 22.5)}')
    if element.get('wind_gust'):
        wind_gust = element['wind_gust']
        weather.append(f'Порывы ветра: {wind_gust} м/с')
    if element.get('clouds'):
        clouds = element['clouds']
        weather.append(f'Облачность: {clouds}%')
    if element.get('pop'):
        pop = element['pop']
        weather.append(f'Вероятность осадков: {round(pop * 100)}%')
    if element.get('rain'):
        if isinstance(element['rain'], dict):
            rain_1h = element['rain']['1h']
            weather.append(f'Дождь: {rain_1h} мм/ч')
        else:
            rain = element['rain']
            weather.append(f'Дождь: {rain} mm')
    if element.get('snow'):
        if isinstance(element['snow'], dict):
            snow = element['snow']['1h']
            weather.append(f'Снег: {snow} мм/ч')
        else:
            snow = element['snow']
            weather.append(f'Снег: {snow} мм')
    if element.get('uvi') and show_long:
        uvi = element['uvi']
        weather.append(f'Индекс УФ: {uvi}')
    if element.get('visibility'):
        visibility = element['visibility']
        weather.append(f'Видимость: {visibility} m')

    return weather


def parse_minutely(minutely_element: dict, timezone_offset: int, show_long: bool = True) -> list[str] | None:
    if minutely_element is None:
        return None
    minutely = []
    if ('dt' in minutely_element) & ('precipitation' in minutely_element):
        minutely_dt = datetime.utcfromtimestamp(minutely_element['dt'] + timezone_offset).strftime('%H:%M')
        minutely_precipitation = minutely_element['precipitation']
        if minutely_precipitation > 0:
            minutely.append(f'Время: {minutely_dt} осадки: {minutely_precipitation} мм/ч')

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
                      f'Согластно {alerts_sender_name} с {alerts_start} по {alerts_end} ожидается {alerts_event}.')
    if 'tags' in alerts_element:
        alerts_tags = alerts_element['tags']

    return alerts


if __name__ == '__main__':
    pass
