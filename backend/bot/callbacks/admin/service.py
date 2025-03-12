from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.common.admin.service import get_admin_service
from bot.utils.filters.callback import PaginatorCallback, ItemCallback
from bot.utils.inline_buttons import item_page_builder
from bot.utils.enums import PageMode
from db.sql.repository import ItemRepository
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
     
     
     async def count_button(
          self,
          session: AsyncSession,
          callback: PaginatorCallback
     ) -> str | tuple[InlineKeyboardMarkup, str]:
          admin_service = await get_admin_service()
          
          markup, image = await admin_service.get_items(
               session=session,
               item="all"
          )
          count_button = markup.inline_keyboard[-1][0] # Inline button с количеством страниц. 1/5
          if count_button.text.split("/")[-1] == str(callback.data_len): # 5 == data_len
               return "Обновление предметов не найдено"  # Если нового предемета в базу не добавлено
          return markup, image
          
          
async def get_callback_admin_service() -> CallbackAdminService:
     return CallbackAdminService()