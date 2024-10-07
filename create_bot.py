from aiogram import Bot, Dispatcher
from os import getenv
from aiogram.enums import ParseMode

TOKEN = getenv("TOKEN")
CHAT_ID = getenv("CHAT_ID")
ADMINS = getenv("ADMINS").split(',')

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)