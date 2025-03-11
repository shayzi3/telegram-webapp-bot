
from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession


from bot.utils.filters.callback import PaginatorCallback, ItemCallback
from bot.utils.inline_buttons import item_page_builder
from bot.utils.enums import PageMode
from db.repository import ItemRepository
from schemas import ItemModel



class CallbackAdminService:
     
     
     async def info_item(
          self,
          session: AsyncSession,
          item_callback:ItemCallback
     ) -> str:
          item = await ItemModel.get_from_redis(item_callback.redis_key)
          if item is None:
               item = await ItemRepository.read(
                    session=session,
                    write_in_redis=True,
                    id=item_callback.id
               )
          if item is None:
               return "Предмет не найден!"
          return item.item_info
          
          
          
          
     async def delete_item(
          self,
          session: AsyncSession,
          item_callback: ItemCallback
     ) -> str:
          ...
          
          
     async def change_item(
          self,
          session: AsyncSession,
          item_callback: ItemCallback
     ) -> str:
          ...
          
          
     async def left_button(
          self,
          session: AsyncSession,
          callback: PaginatorCallback
     ) -> str | tuple[InlineKeyboardMarkup, str]:
          item = await ItemModel.get_from_redis(callback.redis_key_left)
          if item is None:
               item = await ItemRepository.limit_item(
                    session=session,
                    write_in_redis=True,
                    offset=callback.offset - 1,
                    limit=1
               )
          if item is None:
               return "Дальше листать нельзя! Кончились предметы."
          
          markup = item_page_builder(
               data=item,
               mode=PageMode.ALL,
               data_len=callback.data_len,
               offset=callback.offset - 1,
               limit=1
          )
          return markup, item.image
          
          
     async def right_button(
          self,
          session: AsyncSession,
          callback: PaginatorCallback
     ) -> str | tuple[InlineKeyboardMarkup, str]:
          item = await ItemModel.get_from_redis(callback.redis_key_right)
          if item is None:
               item = await ItemRepository.limit_item(
                    session=session,
                    write_in_redis=True,
                    offset=callback.offset + 1,
                    limit=1
               )
          if item is None:
               return "Дальше листать нельзя! Кончились предметы."
          
          markup = item_page_builder(
               data=item,
               mode=PageMode.ALL,
               data_len=callback.data_len,
               offset=callback.offset + 1,
               limit=1
          )
          return markup, item.image
          
          
async def get_callback_admin_service() -> CallbackAdminService:
     return CallbackAdminService()