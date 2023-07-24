from admin.logsetting import logger


def news_view(news_dictionary: dict[int | None, list[float | str | None]] | str) -> str:
    """Return news."""
    if isinstance(news_dictionary, str):
        logger.warning(f'NewsError: {news_dictionary}')
        return news_dictionary
    else:
        result = ''
        for key, value in news_dictionary.items():
            result += f'\n'.join([f'    {i}' for i in value if i is not None])
        return result
