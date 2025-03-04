from aiogram import Bot, Dispatcher
from .config import settings


bot = Bot(settings.bot_token)
dp = Dispatcher()