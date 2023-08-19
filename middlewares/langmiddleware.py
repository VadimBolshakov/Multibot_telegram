from typing import Any, Tuple
from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from databases.database import DataBaseMain as DataBase


class ACLMiddleware(I18nMiddleware):
    """Class for work with i18n (languages)."""
    def __init__(self, domain: str, path: str, db: DataBase):
        self.db = db
        super(ACLMiddleware, self).__init__(domain, path)

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user = types.User.get_current()
        locale = user.locale
        lang = await self.db.get_user_lang_db(user.id)
        return lang or locale
