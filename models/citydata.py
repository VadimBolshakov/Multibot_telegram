"""This module provides functions for getting location by city.

    Get location by city via http://api.openweathermap.org/geo/1.0/direct
    and return dict or string.
"""

from json import JSONDecodeError
from typing import Optional

import aiohttp

import admin.exeptions as ex
from create import TOKEN_OPENWEATHER, logger


async def get_location_by_city(city: str, limit: int = 1, appid: str = TOKEN_OPENWEATHER) -> Optional[list[dict[str, str | int | float]]]:
    """Get location by city.

    Data from http://api.openweathermap.org/geo/1.0/direct

    :param city: city name
    :type city: str
    :param limit: limit of results, defaults to 1
    :type limit: int, optional
    :param appid: token for openweathermap, defaults to TOKEN_OPENWEATHER
    :type appid: str, optional

    :raises ex.ResponseStatusError: if response status not 200
    :raises JSONDecodeError: if response not json
    :raises aiohttp.ClientConnectorError: if connection error

    :return: location
    :rtype: Optional[list[dict[str, str | int | float]]]
    """

    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={appid}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ex.ResponseStatusError(response.status)

                data_location = await response.json()

                return data_location

    except (aiohttp.ClientConnectorError, JSONDecodeError, ex.ResponseStatusError) as e:
        logger.exception(f'LocationError: {str(e)}')
        return None


async def location_dict(city: str = '') -> dict[str, float | str] | str:
    """Parse location from JSON-file and return dict.

    :param city: city name, defaults to ''
    :type city: str, optional

    :return: location
    :rtype: dict[str, float | str] | str
    """
    data_location = await get_location_by_city(city)
    if not data_location:
        return 'Sorry, but we have not information about your city.'

    data_location = data_location[0]

    location = {'name': data_location.get('name'),
                'latitude': data_location.get('lat'),
                'longitude': data_location.get('lon'),
                'country': data_location.get('country'),
                'state': data_location.get('state'),
                }

    return location


if __name__ == '__main__':
    print(location_dict())
