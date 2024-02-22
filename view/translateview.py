"""View for translate text."""


def translate_view(translate_text: dict[str, str] | str) -> str | None:
    """Return text translated into target language.

    :param translate_text: Dictionary with text translated into target language or error.
    :type translate_text: dict[str: str] | str

    :return: Text translated into target language or error.
    :rtype: str
    """
    if isinstance(translate_text, str):
        return translate_text
    return translate_text.get('translate_text')
