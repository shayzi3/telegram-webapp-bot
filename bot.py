import asyncio

from aiogram import Bot, Dispatcher

from bot.handlers.user_commands import start, me
from bot.callbacks import start_callback
from bot.state_machine import register_state
from loguru import logger

from config import settings


async def main() -> None:     
     bot = Bot(settings.key)
     dp = Dispatcher()
     
     logger.info('Bot was created')
     
     dp.include_routers(
          start.router,
          me.router,
          start_callback.router,
          register_state.router
     )
     await bot.delete_webhook(drop_pending_updates=True)
     await dp.start_polling(bot)
     

if __name__ == '__main__':
     asyncio.run(main())
     