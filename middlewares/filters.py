from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


class PrivateFilter(BoundFilter):
    """ Filter for privet messages."""

    async def check(self, message: types.Message) -> bool:
        return message.chat.type == types.ChatType.PRIVATE
