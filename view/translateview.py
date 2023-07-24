from admin.logsetting import logger


def translate_view(translate_text: dict[str] | str) -> str:
    """Return text translated into target language."""
    if isinstance(translate_text, str):
        logger.warning(f'TranslateError: {translate_text}')
        return translate_text
    return translate_text['translatedText']