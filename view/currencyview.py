"""View for currency."""
from typing import Optional


def currency_view(date_now: str, currencies_data: dict[Optional[str], list[Optional[float | str]]] | str) -> str:
    """Return currency.

    :param date_now: Date now.
    :type date_now: str
    :param currencies_data: Dictionary with currencies or error.
    :type currencies_data: dict[Optional[str], list[Optional[float | str]]] | str

    :return: Currency or error.
    :rtype: str
    """
    if isinstance(currencies_data, str):
        return currencies_data
    return f'Currency on {date_now}:\n' + '\n'.join([f'{value[2]} {value[1]} = {value[4]} {value[5]}'
                                                     for key, value in currencies_data.items()])

