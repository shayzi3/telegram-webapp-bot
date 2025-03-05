from random import choice
from string import ascii_letters, digits
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from db.repository import UserRepository, ItemRepository
from .schema import ValidateUrl
from schemas import UserModel, ItemModel


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
          
     
     async def new_item(
          self, 
          session: AsyncSession, 
          data: dict[str, Any]
     ) -> tuple[str, bool]:
          try:
               ValidateUrl(url=data.get("image"))
          except:
               return "URL недействителен! Отправьте повторно", False
          
          data["id"] = self.id_for_item
          await self.item_repository.create(
               session=session,
               **data
          )
          return "Новый предмет добавлен успешно", True
     
     
     async def new_admin(
          self, 
          session: AsyncSession, 
          new_admin_id: str
     ) -> str:
          user = await UserModel.get_from_redis(f"user:{new_admin_id}")
          if user is None:
               user = await self.user_repository.read(
                    session=session,
                    write_in_redis=True,
                    id=new_admin_id
               )
          if user is None:
               return "Такого пользователя не существует!"
          
          if user.is_admin is True:
               return "Пользователь уже является администратором!"

          
          await self.user_repository.update(
               session=session,
               where=user.where,
               clear_in_redis=True,
               is_admin=True
          )
          return "Новый администратор успешно добавлен!"
     
     
     async def delete_item(
          self,
          session: AsyncSession,
          item_id: str
     ) -> str:
          item = ItemModel.get_from_redis(f"item:{item_id}")
          if item is None:
               item = await self.item_repository.read(
                    session=session,
                    write_in_redis=True,
                    id=item_id
               )
          if item is None:
               return "Такого предмета не существует!"
          
          await self.item_repository.delete(
               session=session,
               where=item.where,
               clear_in_redis=True
          )
          return "Предмет успешно удалён"
          
          


async def get_admin_service() -> AdminService:
     return AdminService(
          user_repository=UserRepository(),
          item_repository=ItemRepository()
     )