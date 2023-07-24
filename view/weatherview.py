from admin.logsetting import logger


def weather_view(weather_dict: dict[str, list] | str) -> str:
    if isinstance(weather_dict, str):
        logger.warning(f'WeatherError: {weather_dict}')
        return weather_dict
    result: str = ''
    for key, value in weather_dict.items():
        if isinstance(value[0], list):
            if key not in ('minutely', 'alerts'):
                [item.append('') for item in value]
            result += f'\n'.join([f' {item}' for sublist in value for item in sublist if item is not None])
        else:
            value.append('')
            result += f'\n'.join([f' {item}' for item in value if item is not None])

    return result
