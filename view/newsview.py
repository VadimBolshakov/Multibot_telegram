"""News view module."""
from typing import Generator


def news_view(news_dictionary: dict[int | None, list[float | str | None]] | str) -> Generator:
    """Return news as generator.

    :param news_dictionary: Dictionary with news or error.
    :type news_dictionary: dict[int | None, list[float | str | None]] | str

    :return: News or error.
    :rtype: Generator
    """
    if isinstance(news_dictionary, str):
        return news_dictionary
    else:
        # result = ''
        for key, value in news_dictionary.items():
            yield f'\n'.join([f'    {i}' for i in value if i is not None])
            # result += f'\n'.join([f'    {i}' for i in value if i is not None]) + '\n'
