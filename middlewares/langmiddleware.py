from typing import Any, Tuple
from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from databases import database


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user = types.User.get_current()
        locale = user.locale
        return await database.get_user_lang_db(user.id) or locale
