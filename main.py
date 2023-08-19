"""Main file for the Telegram Bot https://t.me/VadimBolshM1bot.

VadimBolshM1 bot is a Telegram Bot that can send jokes, weather, news, currency_ru, and other information.
username = @VadimBolshM1bot"""
from create import dp, loop, db, i18n, logger
from aiogram.utils import executor
from handlers import general, start, adminhandler, help, changelang, reset


async def on_startup(_):
    """Create database, middlewares, filters and class for work with i18n (languages).
    Also format the logger."""

    if await db.start_db():
        logger.info('DB created')
    else:
        logger.info('DB not created')
    print('Bot in online')
    logger.info('Bot in online')
    _ = i18n.gettext

# try:
start.register_handlers_start(dp)
help.register_handlers_help(dp)
reset.register_handlers_reset(dp)
adminhandler.register_handlers_admin(dp)
changelang.register_handlers_change_lang(dp)
general.register_handlers_general(dp)
# except Exception as e:


async def on_shutdown(_):
    await dp.storage.close()


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
