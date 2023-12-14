"""View for chatgpt."""
from typing import Optional


def chatgpt_view(chatgpt_dictionary: dict[str, str] | str) -> Optional[str]:
    """Return answer.

    :param chatgpt_dictionary: Dictionary with answer or error.
    :type chatgpt_dictionary: dict[str, str] | str

    :return: Answer or None if error.
    :rtype: Optional[str]
    """
    if isinstance(chatgpt_dictionary, str):
        return chatgpt_dictionary
    else:
        return chatgpt_dictionary.get('answer')
