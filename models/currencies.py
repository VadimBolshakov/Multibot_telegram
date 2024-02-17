"""Get an actual rate currency.

If the current language is "ru", get the current exchange rate from the XML file in the src folder.
    If the file does not exist, create a new one and get the exchange rate from cbr.ru.
Otherwise, get the current exchange rate from the JSON file in the src folder.
    If the file does not exist, create a new file and get the exchange rate from the http://apilayer.net/api/live API.
Therefore, we have two functions for getting the currency rate (get_currencies_ru and get_currencies_en),
    and we can get the currency rate from two files depend on language of user.
"""
import asyncio
import json
import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime as dt

import urllib3

import admin.exeptions as ex
from create import TOKEN_CURRENCYLAYER, db, logger


def get_currencies_ru(date_now_str: str, path_file_xml: str) -> bool:
    """Get the actually current exchange cbr.ru and create the XML file.

    :param date_now_str: date in format dd-mm-yyyy
    :type date_now_str: str
    :param path_file_xml: path to XML file
    :type path_file_xml: str

    :raises ex.ResponseStatusError: if response status not 200
    :raises urllib3.exceptions.HTTPError: if connection error

    :return: True if file created, False otherwise
    :rtype: bool
    """
    http = urllib3.PoolManager(num_pools=3)
    try:
        response = http.request('GET', 'https://www.cbr-xml-daily.ru/daily_utf8.xml')
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


async def currencies_dict_ru(user_id: int, first_name: str, lang: str,
                             date_time_now: dt) -> dict[str | None, list[float | str | None]] | str:
    """Get currencies from XML-file and return dict currencies rate or str if data is None.

    :param user_id: user id
    :type user_id: int
    :param first_name: user first name
    :type first_name: str
    :param lang: user language
    :type lang: str
    :param date_time_now: date and time now
    :type date_time_now: dt

    :raises FileNotFoundError: if file not found
    :raises ET.ParseError: if file not XML

    :return: dict with currencies
    :rtype: dict[str | None, list[float | str | None]] | str
    """
    date_time_now_str = date_time_now.strftime("%d-%m-%Y_%H")
    path_file_xml = os.path.normpath(os.path.abspath(f'./src/currency_ru/currencies_{lang}_{date_time_now_str}.xml'))
    if not os.path.isfile(path_file_xml):
        """Delete previous files and create new file."""
        for file in os.scandir(os.path.dirname(path_file_xml)):
            os.remove(file.path)

        try:
            """Create the new actual file."""
            if not get_currencies_ru(date_time_now_str, path_file_xml):
                raise FileNotFoundError

        except FileNotFoundError as e:
            logger.exception(f'CurrencyFileError: {str(e)}. User {first_name} (id:{user_id})')
            await db.add_request_db(user_id=user_id, type_request='currency_ru', num_tokens=0,
                                    status_request=False)
            return 'Sorry, but we have not information about actual currency rate.'
    try:
        tree = ET.parse(path_file_xml)

    except ET.ParseError as e:
        logger.exception(f'CurrencyParseError: {str(e)}. User {first_name} (id:{user_id})')
        await db.add_request_db(user_id=user_id, type_request='currency_ru', num_tokens=0, status_request=False)
        return 'Sorry, but we have not information about actual currency rate.'

    root = tree.getroot()
    currencies = {}
    for child in root:
        currencies[child[1].text] = [
            float(child[i].text.replace(',', '.')) if child[i].tag == 'Value' else child[i].text for i in
            range(len(child))]

    for key, value in currencies.items():
        currencies[key].append('RUB')

    await db.add_request_db(user_id=user_id, type_request='currency_ru', num_tokens=0, status_request=True)
    logger.info(
        f'Exit from currency_ru model user {first_name} (id:{user_id})')
    return currencies


def get_currencies_en(path_file_json: str) -> bool:
    """Get the actually current exchange and create the JSON file.

    :param path_file_json: path to JSON file
    :type path_file_json: str

    :raises ex.ResponseStatusError: if response status not 200
    :raises urllib3.exceptions.HTTPError: if connection error

    :return: True if file created, False otherwise
    :rtype: bool
    """
    http = urllib3.PoolManager(num_pools=3)
    try:
        fields = {
            'access_key': TOKEN_CURRENCYLAYER,
            'currencies': 'RUB,EUR,GBP,JPY,CHF,CNY,UAH,PLN,TRY,CAD,SEK,DKK,NOK,AUD,SGD,BYN,KZT,AMD,IRR,INR,GEL,NZD',
            'source': 'USD',
            'format': 1,
        }
        url = 'http://apilayer.net/api/live'
        response = http.request(method='GET', url=url, fields=fields)

        if not response:
            raise ex.ResponseStatusError(response.status)

        with open(path_file_json, 'w', encoding='utf-8') as f:
            f.write(response.data.decode('utf-8'))
        return True

    except ex.ResponseStatusError as e:
        logger.exception(f'CurrencyError: {str(e)}')
        return False

    except urllib3.exceptions.HTTPError as e:
        logger.exception(f'CurrencyError: {str(e)}')
        return False


async def currencies_dict_en(user_id: int, first_name: str, lang: str,
                             date_time_now: dt) -> dict[str | None, list[float | str | None]] | str:
    """Get currencies from JSON file and return dict currencies rate or str if data is None.

    :param user_id: user id
    :type user_id: int
    :param first_name: user first name
    :type first_name: str
    :param lang: user language
    :type lang: str
    :param date_time_now: date and time now
    :type date_time_now: dt

    :raises FileNotFoundError: if file not found
    :raises json.JSONDecodeError: if file not JSON

    :return: dict with currencies
    :rtype: dict[str | None, list[float | str | None]] | str
    """
    date_time_now_str = date_time_now.strftime("%d-%m-%Y_%H")
    path_file_json = os.path.normpath(os.path.abspath(f'./src/currency_en/currencies_{lang}_{date_time_now_str}.json'))
    if not os.path.isfile(path_file_json):
        """Delete previous files and create new file."""
        for file in os.scandir(os.path.dirname(path_file_json)):
            os.remove(file.path)

        try:
            """Create the new actual file."""
            if not get_currencies_en(path_file_json):
                raise FileNotFoundError

        except FileNotFoundError as e:
            logger.exception(f'CurrencyFileError: {str(e)}. User {first_name} (id:{user_id})')
            await db.add_request_db(user_id=user_id, type_request='currency_en', num_tokens=0,
                                    status_request=False)
            return 'Sorry, but we have not information about actual currency rate.'

    try:
        with open(path_file_json, 'r', encoding='utf-8') as f:
            data_currencies = json.load(f)

    except json.JSONDecodeError as e:
        logger.exception(f'CurrencyParseError: {str(e)}. User {first_name} (id:{user_id})')
        await db.add_request_db(user_id=user_id, type_request='currency_en', num_tokens=0, status_request=False)
        return 'Sorry, but we have not information about actual currency rate.'
    currencies = defaultdict(list)
    for key, value in data_currencies['quotes'].items():
        currencies[key] = ['', key[:3], '', '', value, key[3:]]  # done for compatibility with currencies_dict_ru

    await db.add_request_db(user_id=user_id, type_request='currency_en', num_tokens=0, status_request=True)
    logger.info(
        f'Exit from currency_en model user {first_name} (id:{user_id})')

    return currencies


async def currencies_dict(user_id: int, first_name: str,
                          date_time_now: dt) -> dict[str | None, list[float | str | None]] | str:
    """Return a dict with currencies depend on language of user or str if data is None.

    :param user_id: user id
    :type user_id: int
    :param first_name: user first name
    :type first_name: str
    :param date_time_now: date and time now
    :type date_time_now: dt

    :return: dict with currencies
    :rtype: dict[str | None, list[float | str | None]] | str
    """
    lang = await db.get_user_lang_db(user_id=user_id)
    if lang == 'ru':
        return await currencies_dict_ru(user_id=user_id, first_name=first_name, lang=lang, date_time_now=date_time_now)

    return await currencies_dict_en(user_id=user_id, first_name=first_name, lang=lang, date_time_now=date_time_now)


if __name__ == '__main__':
    date_now = dt.now()
    print(asyncio.run(currencies_dict(user_id=111, first_name='Join', date_time_now=date_now)))
