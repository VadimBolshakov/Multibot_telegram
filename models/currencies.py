"""Get an actual rate currency.

Get actual rate currency from XML-file in src folder.
If file not exist, create a new file and get rate currency form cbr.ru.
"""
import asyncio

import urllib3
import xml.etree.ElementTree as ET
import admin.exeptions as ex
from admin.logsetting import logger
from databases import database
import datetime
import os


def get_currencies(date_now_str: str, path_file_xml: str) -> bool:
    """Get currencies from cbr.ru and create XML-file in src folder."""
    http = urllib3.PoolManager(num_pools=3)
    try:
        response = http.request('GET', 'https://www.cbr.ru/scripts/XML_daily.asp', fields={'date_req': date_now_str})
        if not response:
            raise ex.ResponseStatusError(response.status)

        with open(path_file_xml, 'wb') as f:
            f.write(response.data)
        return True

    except ex.ResponseStatusError as e:
        logger.exception(f'CurrencyError: {str(e)}')
        return False

    except urllib3.exceptions.HTTPError as e:
        logger.exception(f'CurrencyError: {str(e)}')
        return False


async def currencies_dict(user_id: int, first_name: str,
                          date_now_str: str = '21-06-2023', ) -> dict[str | None, list[float | str | None]] | str:
    """Get currencies from XML-file and return dict."""

    path_file_xml = os.path.normpath(os.path.abspath(f'./src/currency/currencies_{date_now_str}.xml'))
    if not os.path.isfile(path_file_xml):
        """Delete previous files and create new file."""
        for file in os.scandir(os.path.dirname(path_file_xml)):
            os.remove(file.path)

    try:
        """Create the new actual file."""
        if not get_currencies(date_now_str, path_file_xml):
            raise FileNotFoundError

        tree = ET.parse(path_file_xml)

    except FileNotFoundError as e:
        logger.exception(f'CurrencyFileError: {str(e)}. User {first_name} (id:{user_id})')
        await database.add_request_db(user_id=user_id, type_request='currency', num_tokens=0, status_request=False)
        return 'Sorry, but we have not information about actual rate currency.'
    except ET.ParseError as e:
        logger.exception(f'CurrencyParseError: {str(e)}. User {first_name} (id:{user_id})')
        await database.add_request_db(user_id=user_id, type_request='currency', num_tokens=0, status_request=False)
        return 'Sorry, but we have not information about actual rate currency.'

    root = tree.getroot()
    currencies = {}
    for child in root:
        currencies[child[1].text] = [
            float(child[i].text.replace(',', '.')) if child[i].tag == 'Value' else child[i].text for i in
            range(len(child))]

    await database.add_request_db(user_id=user_id, type_request='currency', num_tokens=0, status_request=True)
    logger.info(
        f'Exit from currency model user {first_name} (id:{user_id})')
    return currencies


if __name__ == '__main__':
    date_now = datetime.datetime.now().strftime('%d-%m-%Y')
    print(asyncio.run(currencies_dict(user_id=111, first_name='Join', date_now_str=date_now)))
