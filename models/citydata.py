"""This module provides functions for getting location by city."""

import requests
from typing import Optional
import admin.exeptions as ex
from admin.logsetting import logger
from json import JSONDecodeError
from create import TOKEN_OPENWEATHER


def get_location_by_city(city: str, limit: int = 1, appid: str = TOKEN_OPENWEATHER) -> Optional[list[dict[str, str | int | float]]]:
    """Get location by city.

    Data from http://api.openweathermap.org/geo/1.0/direct"""

    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={appid}'

    try:
        response_location = requests.get(url)
        if not response_location:
            raise ex.ResponseStatusError(response_location.status_code)

        data_location = response_location.json()
        return data_location

    except (requests.RequestException, JSONDecodeError, ex.ResponseStatusError) as e:
        logger.exception(f'LocationError: {str(e)}')
        return None


def location_dict(city: str = '') -> dict[str, float | str] | str:
    """Parse location from JSON-file and return dict."""
    data_location = get_location_by_city(city)
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
