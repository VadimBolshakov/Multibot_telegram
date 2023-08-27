"""View for quote."""
from create import logger


def quote_view(quote_dict: dict[str, str | None] | str) -> str:
    """Return quote.

    :param quote_dict: Dictionary with quote or error.
    :type quote_dict: dict[str, str | None] | str

    :return: Quote or error.
    :rtype: str
    """
    if isinstance(quote_dict, str):
        logger.warning(f'QuoteError: {quote_dict}')
        return quote_dict
    else:
        return f'{quote_dict.get("quoteText")}\n{quote_dict.get("quoteAuthor")}'
