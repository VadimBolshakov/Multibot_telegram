from admin.logsetting import logger


def chatgpt_view(chatgpt_dictionary: dict[str, str] | str) -> str:
    """Return answer."""
    if isinstance(chatgpt_dictionary, str):
        logger.warning(f'ChatgptError: {chatgpt_dictionary}')
        return chatgpt_dictionary
    else:
        return chatgpt_dictionary['answer']

