

def jokes_view(jokes_dict: dict[int, str] | str) -> str:
    """Return joke."""
    if isinstance(jokes_dict, str):
        return jokes_dict

    return f'\n\n'.join([f'{value}' for key, value in jokes_dict.items()])

# file from https://github.com/Vl-Leschinskii/jokes_topics/blob/main/anek_utf8.zip
