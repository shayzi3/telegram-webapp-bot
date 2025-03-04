from random import choice
from string import ascii_letters, digits
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.async_container import AsyncContainer

from db.repository import UserRepository, ItemRepository
from .schema import ValidateUrl


class AdminService:
     
     def __init__(
          self, 
          user_repository: UserRepository,
          item_repository: ItemRepository
     ) -> None:
          self.user_repository = user_repository
          self.item_repository = item_repository
          
     
     @property
     def id_for_item(self) -> str:
          symbols = ascii_letters + digits
          return "".join([choice(symbols) for _ in range(20)])
          
     
     async def new_item(self, container: AsyncContainer, data: dict[str, Any]) -> bool:
          try:
               ValidateUrl(url=data.get("image"))
          except:
               return False
          
          data["id"] = self.id_for_item
          session = await container.get(AsyncSession)
          await self.item_repository.create(
               session=session,
               **data
          )
          return True
     
     
     async def new_admin(self, container: AsyncContainer, admin_id: str) -> bool:
          ...
          
          


async def get_admin_service() -> AdminService:
     return AdminService(
          user_repository=UserRepository(),
          item_repository=ItemRepository()
     )