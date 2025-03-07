from random import choice
from string import ascii_letters, digits
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InlineKeyboardMarkup

from bot.utils.enums import PageMode
from bot.utils.inline_buttons import item_page_builder
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
               delete_redis_values=[user.redis_key],
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
               delete_redis_values=[item.redis_key]
          )
          return "Предмет успешно удалён"
     
     
     async def get_items(
          self,
          session: AsyncSession,
          item: str
     ) -> str | tuple[InlineKeyboardMarkup, str]:
          mode = PageMode.ONE
          if item == "all":
               mode = PageMode.ALL
               
          if mode == PageMode.ONE:
               get_item = await ItemModel.get_from_redis(f"item:{item}")
               if get_item is None:
                    get_item = await self.item_repository.read(
                         session=session,
                         write_in_redis=True,
                         id=item
                    )
                    
          elif mode == PageMode.ALL:
               get_item = await ItemModel.get_from_redis(f"item:off={0}lim={1}")
               if get_item is None:
                    get_item = await self.item_repository.limit_item(
                         session=session,
                         write_in_redis=True,
                         offset=0,
                         limit=1,
                    )
               item_len = await self.item_repository.get_count_items(
                    session=session
               )
               
          if get_item is None:
               return "Такого предмета не существует!"
          
          page_build = item_page_builder(
               data=get_item,
               mode=mode,
               offset=0,
               limit=1,
               data_len=item_len
          )
          return page_build, get_item.image
          


async def get_admin_service() -> AdminService:
     return AdminService(
          user_repository=UserRepository,
          item_repository=ItemRepository
     )