

def currency_view(date_now: str, currencies_data: dict[str | None, list[float | str | None]] | str) -> str:
    if isinstance(currencies_data, str):
        return currencies_data
    return f'Currency on {date_now}:\n' + '\n'.join([f'{value[2]} {value[1]} = {value[4]} RUB' for key, value in currencies_data.items()])
