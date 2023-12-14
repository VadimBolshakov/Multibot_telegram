"""Create bot, dispatcher, storage and load environment variables."""
import asyncio
import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from admin.logsetting import logger as setuplogging
from databases.database import DataBaseMain
from middlewares import setup_middleware_i18n, setup_middlewares_filters

load_dotenv(find_dotenv())

DB_NAME: Optional[str] = os.getenv('DB_NAME')
DB_USER: Optional[str] = os.getenv('DB_USER')
DB_PASSWORD: Optional[str] = os.getenv('DB_PASSWORD')
DB_HOST: Optional[str] = os.getenv('DB_HOST')
DB_PORT: Optional[str] = os.getenv('DB_PORT')
GPT_API_KEY: Optional[str] = os.getenv('GPT_API_KEY')
CHAT_ID: Optional[str] = os.getenv('CHAT_ID')
ADMIN_ID: Optional[str] = os.getenv('ADMIN_ID')
PASSWORD: Optional[str] = os.getenv('PASSWORD')
TOKEN_BOT: Optional[str] = os.getenv('TOKEN_BOT')
TOKEN_OPENWEATHER: Optional[str] = os.getenv('TOKEN_OPENWEATHER')
TOKEN_NEWSAPI: Optional[str] = os.getenv('TOKEN_NEWSAPI')
TOKEN_GOOGLE_TRANSLATE: Optional[str] = os.getenv('TOKEN_GOOGLE_TRANSLATE')
TOKEN_CURRENCYLAYER: Optional[str] = os.getenv('TOKEN_CURRENCYLAYER')
FOUL_FILE: Optional[str] = os.getenv('FOUL_FILE')
LOG_FILE: Optional[str] = os.getenv('LOG_FILE')

I18N_DOMAIN = 'base'

BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'


loop = asyncio.new_event_loop()
# loop = asyncio.get_event_loop()
logger = setuplogging

db = DataBaseMain(db_user=DB_USER, db_password=DB_PASSWORD, db_host=DB_HOST, db_port=DB_PORT, db_name=DB_NAME, logger=logger)

bot = Bot(TOKEN_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)

i18n = setup_middleware_i18n(dp, domain=I18N_DOMAIN, locales_dir=LOCALES_DIR, db=db)
setup_middlewares_filters(dp, password=PASSWORD, foul_file=FOUL_FILE, db=db, logger=logger)
