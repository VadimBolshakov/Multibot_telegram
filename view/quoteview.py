from admin.logsetting import logger


def quote_view(quote_dict: dict[str, str | None] | str) -> str:
    """Return quote."""
    if isinstance(quote_dict, str):
        logger.warning(f'QuoteError: {quote_dict}')
        return quote_dict
    else:
        return f'{quote_dict.get("quoteText")}\n{quote_dict.get("quoteAuthor")}'
