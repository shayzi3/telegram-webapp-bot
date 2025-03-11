from typing import AsyncGenerator
from dishka import Provider, Scope, provide, make_async_container
from dishka.integrations.aiogram import AiogramProvider
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.common.user.service import UserService, get_user_service
from bot.handlers.common.admin.service import AdminService, get_admin_service
from bot.callbacks.admin.service import CallbackAdminService, get_callback_admin_service
from db.session import Session




class InjectProvider(Provider):
     
     @provide(scope=Scope.APP)
     async def get_user_service(self) -> UserService:
          return await get_user_service()
     
     
     @provide(scope=Scope.APP)
     async def get_admin_service(self) -> AdminService:
          return await get_admin_service()
     
     
     @provide(scope=Scope.APP)
     async def get_callback_admin_server(self) -> CallbackAdminService:
          return await get_callback_admin_service()
     
     
     @provide(scope=Scope.APP)
     async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
          async with Session.async_session() as session:
               try:
                    yield session
               finally:
                    await session.close()
     
     
container = make_async_container(InjectProvider(), AiogramProvider())
          