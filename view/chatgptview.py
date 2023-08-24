from typing import Optional


def chatgpt_view(chatgpt_dictionary: dict[str, str] | str) -> Optional[str]:
    """Return answer."""
    if isinstance(chatgpt_dictionary, str):
        return chatgpt_dictionary
    else:
        return chatgpt_dictionary.get('answer')

