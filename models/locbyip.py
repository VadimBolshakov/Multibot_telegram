import aiohttp
import admin.exeptions as ex
from admin.logsetting import logger
from json import JSONDecodeError


async def get_location_by_ip(ip: str = '') -> dict[str, str] | None:
    """Get location by IP."""
    # try:
    #     response_location = requests.get(f'http://ip-api.com/json/{ip}?fields=lat,lon')
    #     if not response_location:
    #         raise ex.ResponseStatusError(response_location.status_code)
    #
    #     data_location = response_location.json()
    #     with open('location.json', 'w') as file:
    #         dump(data_location, file, indent=4, ensure_ascii=False)
    #     return data_location
    #
    # except (requests.RequestException, JSONDecodeError, ex.ResponseStatusError) as e:
    #     logger.exception(f'LocationError: {str(e)}')
    #     return None
    url = 'http://ipinfo.io/json'

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


async def location_dict(ip: str = '') -> dict[str, float | str] | str:
    """Parse location from JSON-file and return dict."""
    data_location = await get_location_by_ip(ip)
    if not data_location:
        return 'Sorry, but we have not information about your location.'

    location = {'ip': data_location['ip'],
                'city': data_location['city'],
                'region': data_location['region'],
                'country': data_location['country'],
                'latitude': float(data_location['loc'].split(',')[0]),
                'longitude': float(data_location['loc'].split(',')[1]),
                'org': data_location['org'],
                'timezone': data_location['timezone']}
    return location


if __name__ == '__main__':
    print(location_dict())
