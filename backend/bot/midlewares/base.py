from typing import Any, Callable, Awaitable
from datetime import datetime, timedelta
from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from db.repository import UserRepository
from bot.provider import container
from schemas import UserModel
from core import settings



class TimeoutMiddleware(BaseMiddleware):
     users = {}
     
     
     async def __call__(
          self, 
          handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], 
          event: Message, 
          data: dict[str, Any]
     ) -> None:
          if event.from_user.id not in self.users:
               self.users[event.from_user.id] = datetime.utcnow() + timedelta(seconds=1)
               return await handler(event, data)
               
          if self.users[event.from_user.id] > datetime.utcnow():
               return await event.answer("Ограничение отправки команды в 1 секунду!")
          
          self.users[event.from_user.id] = datetime.utcnow() + timedelta(seconds=1)
          return await handler(event, data)
     
     
     
class IsAdminMiddleware(BaseMiddleware):
     
     async def __call__(
          self, 
          handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], 
          event: Message, 
          data: dict[str, Any]
     ) -> None:
          if event.from_user.id in settings.admins:
               return await handler(event, data)
          
          
          user = await UserModel.get_from_redis(f"user:{event.from_user.id}")
          if user is None:
               session = await container.get(AsyncSession)
               user = await UserRepository().read(
                    session=session,
                    write_in_redis=True,
                    id=event.from_user.id
               )
               
          if user.is_admin is False:
               return await event.answer("Вы не администратор!")
          return await handler(event, data)