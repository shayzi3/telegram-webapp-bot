from typing import Any, Callable, Awaitable
from datetime import datetime, timedelta
from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from db.sql.session import get_async_session
from db.sql.repository import UserRepository
from core import settings



class TimeoutMiddleware(BaseMiddleware):
     users = {}
     
     
     def __init__(self, rate_limit: int = 1):
          self.rate_limit = rate_limit
     
     
     async def __call__(
          self, 
          handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], 
          event: Message, 
          data: dict[str, Any]
     ) -> None:
          if event.from_user.id not in self.users:
               self.users[event.from_user.id] = datetime.utcnow() + timedelta(seconds=self.rate_limit)
               return await handler(event, data)
               
          if self.users[event.from_user.id] > datetime.utcnow():
               return await event.answer("Ограничение отправки команды в 1 секунду!")
          
          self.users[event.from_user.id] = datetime.utcnow() + timedelta(seconds=self.rate_limit)
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
          
          session = await get_async_session()
          user = await UserRepository.read(
               session=session,
               write_in_redis=True,
               redis_get_value=f"user:{event.from_user.id}",
               id=event.from_user.id
          )
          if user.is_admin is False:
               return await event.answer("Вы не администратор!")
          return await handler(event, data)
     
     
class LogMiddleware(BaseMiddleware):
     
     async def __call__(
          self, 
          handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], 
          event: Message, 
          data: dict[str, Any]
     ) -> None:
          ...