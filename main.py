"""Main file for the Telegram Bot https://t.me/VadimBolshM1bot.

VadimBolshM1 bot is a Telegram Bot that can send jokes, weather, news, currency, and other information.
username = @VadimBolshM1bot"""

from create import dp, bot
from admin.logsetting import logger
from aiogram.utils import executor
from handlers import general, start, adminhandler, help
from databases import database
import asyncio


async def on_startup(_):
    print('Bot in online')
    logger.info('Bot in online')
    await database.start_db()
    # await asyncio.get_event_loop().run_until_complete(database.start_db())
    logger.info('DB created')

start.register_handlers_start(dp)
help.register_handlers_help(dp)
adminhandler.register_handlers_admin(dp)
general.register_handlers_general(dp)

# sendadmin.register_handlers_sendadmin(dp)


async def on_shutdown():
    await bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

