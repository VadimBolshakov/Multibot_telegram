

def translate_view(translate_text: dict[str: str] | str) -> str:
    """Return text translated into target language."""
    if isinstance(translate_text, str):
        return translate_text
    return translate_text.get('translate_text')
