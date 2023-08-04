from typing import Any, Tuple
from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from databases import database
from create import I18N_DOMAIN, LOCALES_DIR


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user = types.User.get_current()
        locale = user.locale
        return await database.get_user_lang_db(user.id) or locale


def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
