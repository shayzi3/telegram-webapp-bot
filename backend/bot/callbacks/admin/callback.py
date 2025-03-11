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
from bot.handlers.common.admin.service import AdminService
from schemas import ItemModel
from .service import CallbackAdminService


admin_callback_router = Router(name="admin_callback_router")



@admin_callback_router.callback_query(ItemCallback.filter(F.filter_mode == "delete"))
async def delete_item(query: CallbackQuery, callback_data: ItemCallback) -> None:
     ...
     
     
     
@admin_callback_router.callback_query(ItemCallback.filter(F.filter_mode == "change"))
async def change_item(query: CallbackQuery, callback_data: ItemCallback) -> None:
     ...
     
     
     
@admin_callback_router.callback_query(ItemCallback.filter(F.filter_mode == "info"))
@inject
async def info_item(
     query: CallbackQuery, 
     callback_data: ItemCallback,
     session: FromDishka[AsyncSession],
     service: FromDishka[CallbackAdminService]
) -> None:
     result = await service.info_item(
          session=session,
          item_callback=callback_data
     )
     await query.message.answer(result, reply_markup=delete_message)
     await query.answer()
     
     

@admin_callback_router.callback_query(PaginatorCallback.filter(F.paginate_mode == "left"))
@inject
async def left_button(
     query: CallbackQuery, 
     callback_data: PaginatorCallback,
     session: FromDishka[AsyncSession],
     service: FromDishka[CallbackAdminService]
) -> None:
     if callback_data.offset <= 0:
          return await query.answer("Листать дальше нельзя!")
     
     result = await service.left_button(
          session=session,
          callback=callback_data
     )
     if isinstance(result, str):
          return await query.answer(result)
     
     await query.message.edit_media(
          media=InputMediaPhoto(media=result[1]),
          reply_markup=result[0]
     )
     
     

@admin_callback_router.callback_query(PaginatorCallback.filter(F.paginate_mode == "right"))
@inject
async def right_button(
     query: CallbackQuery, 
     callback_data: PaginatorCallback,
     session: FromDishka[AsyncSession],
     service: FromDishka[CallbackAdminService]
) -> None:
     if callback_data.offset + 1 >= callback_data.data_len:
          return await query.answer("Листать дальше нельзя!")
     
     result = await service.right_button(
          session=session,
          callback=callback_data
     )
     if isinstance(result, str):
          return await query.answer(result)
     
     await query.message.edit_media(
          media=InputMediaPhoto(media=result[1]),
          reply_markup=result[0]
     )
     
     
@admin_callback_router.callback_query(PaginatorCallback.filter(F.paginate_mode == "count"))
@inject
async def count_button(
     query: CallbackQuery,
     callback_data: PaginatorCallback,
     session: FromDishka[AsyncSession],
     service: FromDishka[AdminService]
) -> None:
     markup, image = await service.get_items(
          session=session,
          item="all"
     )
     count_button = markup.inline_keyboard[-1][0] # Inline button with text count pages. 1/5
     if count_button.text.split("/")[-1] == str(callback_data.data_len): # 5 == data_len
          return await query.answer("Обновление предметов не найдено") # Если нового предемета в базу не добавлено
     
     await query.message.edit_media(
          media=InputMediaPhoto(media=image),
          reply_markup=markup
     )
     
     
     
     
