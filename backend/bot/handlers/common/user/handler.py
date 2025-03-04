from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from bot.utils.inline_buttons import webapp_button_builder
from .service import UserService


user_router = Router(name=__name__)


@user_router.message(CommandStart())
@inject
async def start(
     message: Message,
     service: FromDishka[UserService]
) -> None:
     text = f"Совершай покупки в WebApp приложении!"
     await service.start(
          id=message.from_user.id,
          name=message.from_user.full_name,
          container=message.dishka,
     )
     await message.answer(
          text=text, 
          reply_markup=webapp_button_builder(message.from_user.id),
     )
     
     
          
     