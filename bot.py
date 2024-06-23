import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.handlers.user_commands import start
from bot.callbacks import start_callback
from bot.state_machine import register_state
from config import settings


logger = logging.getLogger(__name__)


async def main() -> None:
     logging.basicConfig(level=logging.INFO)
     
     bot = Bot(settings.key)
     dp = Dispatcher()
     
     dp.include_routers(
          start.router,
          start_callback.router,
          register_state.router
     )
     
     logger.info('Bot was started.')
     
     await bot.delete_webhook(drop_pending_updates=True)
     await dp.start_polling(bot)
     

if __name__ == '__main__':
     asyncio.run(main())
     