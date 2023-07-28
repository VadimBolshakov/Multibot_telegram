"""Main file for the Telegram Bot https://t.me/VadimBolshM1bot.

VadimBolshM1 bot is a Telegram Bot that can send jokes, weather, news, currency_ru, and other information.
username = @VadimBolshM1bot"""

from create import dp, loop
from aiogram.utils import executor
from admin.logsetting import logger
from handlers import general, start, adminhandler, help, changelang
from databases import database


async def on_startup(_):
    print('Bot in online')
    logger.info('Bot in online')
    await database.start_db()
    logger.info('DB created')

# loop.run_until_complete(database.start_db())
start.register_handlers_start(dp)
help.register_handlers_help(dp)
adminhandler.register_handlers_admin(dp)
changelang.register_handlers_change_lang(dp)
general.register_handlers_general(dp)


async def on_shutdown(_):
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
