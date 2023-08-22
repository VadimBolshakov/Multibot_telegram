"""Get random string from json file

This module is used to get random string from json file.

The file must be in the following format:
{'1': 'string1', '2': 'string2', '3': 'string3', ...}
Example:
    get_random_str('./src/foul/quote_against_foul.json')

    Output:
        string1"""
import json
import random


def get_random_string(path: str) -> str:
    """Get random string from json file.

    Args:
        path (str): Path to json file.

    Returns:
        str: Random string from json file.
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data[str(random.randint(1, len(data)))]
