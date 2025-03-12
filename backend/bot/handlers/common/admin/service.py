from random import choice
from string import digits
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InlineKeyboardMarkup

from bot.utils.enums import PageMode
from bot.utils.inline_buttons import item_page_builder
from db.sql.repository import UserRepository, ItemRepository
from schemas import UserModel, ItemModel
from .schema import ValidateUrl



class AdminService:
          
     
     @property
     def id_for_item(self) -> str:
          return "".join([choice(digits) for _ in range(5)])
          
     
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
          await ItemRepository.create(
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
               user = await UserRepository.read(
                    session=session,
                    write_in_redis=True,
                    id=new_admin_id
               )
          if user is None:
               return "Такого пользователя не существует!"
          
          if user.is_admin is True:
               return "Пользователь уже является администратором!"

          
          await UserRepository.update(
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
          item = await ItemModel.get_from_redis(f"item:{item_id}")
          if item is None:
               item = await ItemRepository.read(
                    session=session,
                    write_in_redis=True,
                    id=item_id
               )
          if item is None:
               return "Такого предмета не существует!"
          
          await ItemRepository.delete(
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
               
          item_len = 0
          if mode == PageMode.ONE:
               get_item = await ItemModel.get_from_redis(f"item:{item}")
               if get_item is None:
                    get_item = await ItemRepository.read(
                         session=session,
                         write_in_redis=True,
                         id=item
                    )
                    
          elif mode == PageMode.ALL:
               get_item = await ItemModel.get_from_redis(f"item:off={0}lim={1}")
               if get_item is None:
                    get_item = await ItemRepository.limit_item(
                         session=session,
                         write_in_redis=True,
                         offset=0,
                         limit=1,
                    )
               item_len = await ItemRepository.get_count_items(
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
     
     
     async def admins(
          session: AsyncSession
     ) -> None:
          ...
          
          
     async def new_item_doc(
          session: AsyncSession,
          document: bytes
     ) -> None:
          ...
          


async def get_admin_service() -> AdminService:
     return AdminService()