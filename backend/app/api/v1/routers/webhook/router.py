from fastapi import APIRouter, Request, Response, Depends
from aiogram.types import Update

from core import bot, dp
from integration.yoomoney import yoomoney_client, YoomoneyResponse
from app.api.dependecies.webhook import secret_aiogram, secret_yoomoney


webhook_router = APIRouter(prefix="/api/v1", tags=["Webhook"])


@webhook_router.post(path="/aiogram_webhook", dependencies=[Depends(secret_aiogram)])
async def aiogram_webhook(request: Request) -> Response:
     update = Update.model_validate(await request.json(), context={"bot": bot})
     await dp.feed_update(bot, update)
     return Response()



@webhook_router.post(path="/yoomoney_webhook", dependencies=[Depends(secret_yoomoney)])
async def yoomoney_webhook(request: Request) -> Response:
     data = await request.body()
     split_data = data.decode().split("&")

     kwargs = {}
     for arg in split_data:
          name = arg.split("=")
          kwargs[name[0]] = name[1] if len(name) > 1 else "" 
          
     await yoomoney_client.on_success(
          response=YoomoneyResponse.model_validate(kwargs), 
          bot=bot
     )
     return Response()