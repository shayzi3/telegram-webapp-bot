from aiogram.types.callback_query import CallbackQuery
from aiogram.types import InputMediaPhoto
from aiogram import F, Router
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.aiogram import inject
from dishka import FromDishka

from db.repository import ItemRepository
from bot.utils.inline_buttons import item_page_builder
from bot.utils.enums import PageMode
from bot.utils.filters.callback import ItemCallback, PaginatorCallback
from bot.utils.inline_buttons import delete_message
from schemas import ItemModel


admin_callback_router = Router(name="admin_callback_router")



@admin_callback_router.callback_query(ItemCallback.filter(F.filter_mode == "delete"))
async def delete_item(query: CallbackQuery, callback_data: ItemCallback) -> None:
     ...
     
     
     
@admin_callback_router.callback_query(ItemCallback.filter(F.filter_mode == "change"))
async def change_item(query: CallbackQuery, callback_data: ItemCallback) -> None:
     ...
     
     
     
@admin_callback_router.callback_query(ItemCallback.filter(F.filter_mode == "info"))
async def info_item(query: CallbackQuery, callback_data: ItemCallback) -> None:
     await query.message.answer(callback_data.to_info, reply_markup=delete_message)
     await query.answer()
     
     

@admin_callback_router.callback_query(PaginatorCallback.filter(F.paginate_mode == "left"))
@inject
async def left_button(
     query: CallbackQuery, 
     callback_data: PaginatorCallback,
     session: FromDishka[AsyncSession]
) -> None:
     if callback_data.offset <= 0:
          return await query.answer("Листать дальше нельзя!")
     
     item = await ItemModel.get_from_redis(f"item:off={callback_data.offset - 1}lim={callback_data.limit}")
     if item is None:
          item = await ItemRepository.limit_item(
               session=session,
               write_in_redis=True,
               offset=callback_data.offset - 1,
               limit=1
          )
     if item is None:
          return await query.answer("Дальше листать нельзя! Кончились предметы.")
     
     markup = item_page_builder(
          data=item,
          mode=PageMode.ALL,
          data_len=callback_data.data_len,
          offset=callback_data.offset - 1,
          limit=1
     )
     await query.message.edit_media(
          media=InputMediaPhoto(media=item.image),
          reply_markup=markup
     )
     
     

@admin_callback_router.callback_query(PaginatorCallback.filter(F.paginate_mode == "right"))
@inject
async def right_button(
     query: CallbackQuery, 
     callback_data: PaginatorCallback,
     session: FromDishka[AsyncSession]
) -> None:
     if callback_data.offset + 1 >= callback_data.data_len:
          return await query.answer("Листать дальше нельзя!")
     
     item = await ItemModel.get_from_redis(f"item:off={callback_data.offset + 1}lim={callback_data.limit}")
     if item is None:
          item = await ItemRepository.limit_item(
               session=session,
               write_in_redis=True,
               offset=callback_data.offset + 1,
               limit=1
          )
     if item is None:
          return await query.answer("Дальше листать нельзя! Кончились предметы.")
     
     markup = item_page_builder(
          data=item,
          mode=PageMode.ALL,
          data_len=callback_data.data_len,
          offset=callback_data.offset + 1,
          limit=1
     )
     await query.message.edit_media(
          media=InputMediaPhoto(media=item.image),
          reply_markup=markup
     )
     
     
     
