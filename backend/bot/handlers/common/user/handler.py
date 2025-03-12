from typing import Optional
from aiogram.types import Message
from aiogram.methods import SendMessage
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.aiogram import inject
from dishka import FromDishka

from bot.utils.inline_buttons import webapp_button_builder
from .service import UserService


user_router = Router(name="user_router")


@user_router.message(CommandStart())
@inject
async def start(
     message: Message,
     session: FromDishka[AsyncSession],
     service: FromDishka[UserService]
) -> None:
     result = await service.start(
          id=message.from_user.id,
          name=message.from_user.full_name,
          session=session,
     )
     await message.answer(
          text=result, 
          reply_markup=webapp_button_builder(message.from_user.id),
     )
     
     
@user_router.message(Command("skip"))
async def skip(message: Message, state: FSMContext) -> Optional[SendMessage]:
     active_state = await state.get_state()
     if active_state:
          await state.clear()
          return await message.answer("Событие пропущено")
     await message.answer("Событий не найдено")
     
     
@user_router.message(Command("basket"))
async def basket(message: Message) -> None:
     ...
     
     
@user_router.message(Command("buy"))
async def buy(message: Message) -> None:
     ...     
     
          
     