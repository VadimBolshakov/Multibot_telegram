"""Create bot, dispatcher, storage and load environment variables."""
import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv(find_dotenv())

EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
GPT_API_KEY = os.getenv('GPT_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')
ADMIN_ID = os.getenv('ADMIN_ID')
PASSWORD = os.getenv('PASSWORD')
TOKEN_BOT = os.getenv('TOKEN_BOT')
TOKEN_OPENWEATHER = os.getenv('TOKEN_OPENWEATHER')
TOKEN_NEWSAPI = os.getenv('TOKEN_NEWSAPI')
TOKEN_GOOGLE_TRANSLATE = os.getenv('TOKEN_GOOGLE_TRANSLATE')
LOG_FILE = os.getenv('LOG_FILE')

loop = asyncio.get_event_loop()
bot = Bot(TOKEN_BOT, loop=loop)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

