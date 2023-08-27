"""Create menu on different languages (Internationalize your bot) from list in aiogram.
    Menu inline and menu reply keyboard.
"""
import json
from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create import db, logger


async def create_menu_inline(name_menu: str,
                             language: Optional[str] = None,
                             user_id: Optional[int] = None) -> Optional[InlineKeyboardMarkup]:
    """
    Create menu inline from json file.

    :param name_menu: Name menu to get from Json file.
    :type name_menu: str
    :param language: Language. If None then get language from database.
    :type language: Optional(str)
    :param user_id: User id. Necessary if language is None.
    :type user_id: Optional(int)

    :raises TypeError: If language is None and user_id is None.
    :raises FileNotFoundError: If file not found.
    :raises JSONDecodeError: If json file is not valid.

    :return: Menu inline or None if error.
    :rtype: A: class: `Optional(InlineKeyboardMarkup)`
    """

    if language is None:
        try:
            language = await db.get_user_lang_db(user_id=user_id)
        except TypeError as e:
            logger.exception(f'Error: {str(e)}')
            return None

    path = './src/menu/menu_' + language + '.json'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except [FileNotFoundError, json.JSONDecodeError] as e:
        logger.exception(f'Error: {str(e)}')
        return None

    menu_inline_list = data[name_menu]

    menu = InlineKeyboardMarkup(row_width=2)
    list_keyboards = []
    count = 0
    for key, value in menu_inline_list.items():
        list_keyboards.append(InlineKeyboardButton(text=value, callback_data=key))
        count += 1
        if count == 2:
            menu.add(*list_keyboards)
            count = 0
            list_keyboards = []

    if list_keyboards:
        menu.add(*list_keyboards)

    return menu


if __name__ == '__main__':
    pass
