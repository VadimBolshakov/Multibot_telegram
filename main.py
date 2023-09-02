"""
Main file for the Telegram Bot https://t.me/VadimBolshM1bot.

VadimBolshM1 bot is a Telegram Bot that can send jokes, weather, news, currency_ru, and other information.
username = @VadimBolshM1bot
"""
from aiogram.utils import executor

from create import dp, loop, db, i18n, logger
from handlers import general, start, adminhandler, help, changelang, reset
from util.texttojson import convert_text_files_to_json


async def on_startup(_):
    """Create database, class for work with i18n (languages), also format the logger."""
    if await db.start_db():
        logger.info('DB created')
    else:
        logger.info('DB not created')
    if convert_text_files_to_json('./src/menu/', logger=logger):
        logger.info('Menu created')
    logger.info('Bot in online')
    _ = i18n.gettext

# try:
start.register_handlers_start(dp)
help.register_handlers_help(dp)
reset.register_handlers_reset()
adminhandler.register_handlers_admin(dp)
changelang.register_handlers_change_lang()
general.register_handlers_general(dp)
# except Exception as e:


async def on_shutdown(_):
    """Close memory."""
    await dp.storage.close()


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
