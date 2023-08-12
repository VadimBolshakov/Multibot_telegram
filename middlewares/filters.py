from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from databases import database


class AdminFilter(BoundFilter):
    """ Filter for admins."""
    async def check(self, message: types.Message) -> bool:
        return await database.get_user_admin_db(message.from_user.id)


class PrivateFilter(BoundFilter):
    """ Filter for privet messages."""
    async def check(self, message: types.Message) -> bool:
        return message.chat.type == types.ChatType.PRIVATE
