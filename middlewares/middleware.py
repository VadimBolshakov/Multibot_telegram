"""Middleware module for aiogram

This module contains the manage middleware and the admin filter."""
import asyncio
import json
import string

from aiogram import types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT, Dispatcher
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from databases import database

from admin.logsetting import logger


# Default rate limit set in DEFAULT_RATE_LIMIT = 0.1 seconds


class ManageMiddleware(BaseMiddleware):
    """Manage middleware.

    This middleware checks user ban, registration, and flood.
    Anti-flood middleware is used from https://docs.aiogram.dev/en/latest/examples/middleware_and_antiflood.html."""

    def __init__(self, *, password: str, foul_file: str, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.password = password
        self.foul_set = self._foul_as_set(foul_file)
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ManageMiddleware, self).__init__()

    def _foul_as_set(self, foul_file: str) -> set:
        """Return set of words from user text."""
        foul_set = set()
        try:
            with open(foul_file, encoding='utf-8') as file:
                foul_set = json.load(file)
        except FileNotFoundError:
            logger.warning('Foul file not found')
        return foul_set

    async def on_pre_process_update(self, update: types.Update, data: dict):
        """Check the user in the database and check the user ban."""
        message_text: str | None = None
        if update.message:
            user_id = update.message.from_user.id
            message_text = update.message.text
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        elif update.inline_query:
            user_id = update.inline_query.from_user.id
        elif update.chosen_inline_result:
            user_id = update.chosen_inline_result.from_user.id
        elif update.shipping_query:
            user_id = update.shipping_query.from_user.id
        elif update.pre_checkout_query:
            user_id = update.pre_checkout_query.from_user.id
        else:
            return
        try:

            if await database.get_user_db(user_id) is None:
                if message_text != '/start' and message_text != self.password:
                    if update.message:
                        await update.message.answer(f"You are not registered. Enter the command /start")
                    elif update.callback_query:
                        await update.callback_query.answer(f"You are not registered. Enter the command /start")
                    logger.warning(f'Fail the registration check user id:{user_id}')
                    raise CancelHandler()
                # # if registration is without password then add user to db
                # else:
                #     await database.add_user_db(user_id, update.message.from_user.first_name)
                #     await update.message.answer(f"Hello, {update.message.from_user.first_name}! You are registered")

            if await database.get_user_banned_db(user_id):
                if update.message:
                    await update.message.answer('You are banned')
                elif update.callback_query:
                    await update.callback_query.answer('You are banned')
                logger.warning(f'Fail the ban check user id:{user_id}')
                raise CancelHandler()

        except Exception as e:
            logger.exception(f'Error {str(e)} for update user id:{user_id}')
            raise CancelHandler()

    async def on_process_message(self, message: types.Message, data: dict):
        """Check the foul language and the throttling rate limit for message handler."""
        handler = current_handler.get()

        dispatcher = Dispatcher.get_current()

        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        user_id = message.from_user.id
        user_first_name = message.from_user.first_name

        try:
            if message.text is not None:
                if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
                        .intersection(self.foul_set):
                    await message.reply('foul language is prohibited')
                    if message: await message.delete()
                    logger.warning(f'Fail the foul language check user {user_first_name} (id:{user_id})')
                    raise CancelHandler()
            await dispatcher.throttle(key, rate=limit)

        except Throttled as t:
            # Execute action
            await self.message_throttled(message, t)
            raise CancelHandler()

        except Exception as e:
            logger.exception(f'Error {str(e)} for update user {user_first_name} (id:{user_id})')
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        """
        Notify user only on first exceed and notify about unlocking only on last exceed

        :param message:
        :param throttled:
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        # Calculate how many time is left till the block ends
        delta = throttled.rate - throttled.delta

        # Prevent flooding
        if throttled.exceeded_count <= 2:
            await message.reply('Too many requests! ')

        # Sleep.
        await asyncio.sleep(delta)

        # Check lock status
        thr = await dispatcher.check_key(key)

        # If current message is not last with current key - do not send message
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('Unlocked.')

        return message

    async def on_process_callback_query(self, callback_query, data):
        """Check the throttling rate limit for callback_query handler."""
        handler = current_handler.get()

        dispatcher = Dispatcher.get_current()

        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        user_id = callback_query.from_user.id

        try:
            await dispatcher.throttle(key, rate=limit)

        except Throttled as t:
            # Execute action
            await self.message_throttled(callback_query, t)
            raise CancelHandler()

        except Exception as e:
            logger.exception(f'Error {str(e)} for update user id:{user_id}')
            raise CancelHandler()

