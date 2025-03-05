import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager
from dishka.integrations.aiogram import setup_dishka

from bot.handlers import __routers__
from app.api.v1.routers import __api_routers__
from core import bot, dp, settings
from bot.midlewares import TimeoutMiddleware
from bot.provider import container



@asynccontextmanager
async def lifespan(_: FastAPI):
     dp.include_routers(*__routers__)
     dp.message.middleware(TimeoutMiddleware())
     
     setup_dishka(container=container, router=dp, auto_inject=True)
     
     await bot.set_webhook(
          url=settings.aiogram_webhook,
          drop_pending_updates=True,
          allowed_updates=dp.resolve_used_update_types()
     )
     yield
     await container.close()
     await bot.delete_webhook(drop_pending_updates=True)



app = FastAPI(lifespan=lifespan)
for route in __api_routers__:
     app.include_router(route)
     


if __name__ == '__main__':
     uvicorn.run("main:app", host="0.0.0.0", port=8083, reload=True)
     