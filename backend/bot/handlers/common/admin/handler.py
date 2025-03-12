from typing import Optional
from aiogram import Router, F
from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message
from aiogram.methods import SendMessage
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.aiogram import inject
from dishka import FromDishka

from bot.utils.states import NewItemState, NewItemDocState
from bot.midlewares import IsAdminMiddleware
from .service import AdminService


admin_router = Router(name="admin_router")
admin_router.message.middleware(IsAdminMiddleware())



@admin_router.message(Command("new_item"))
async def new_item(message: Message, state: FSMContext) -> None:
     await state.clear()
     await state.set_state(NewItemState.name)
     await message.answer("Название товара")
     

@admin_router.message(NewItemState.name, F.text)
async def new_item_name(message: Message, state: FSMContext) -> None:
     await state.update_data(name=message.text)
     await state.set_state(NewItemState.description)
     await message.answer("Описание товара")
     
     
@admin_router.message(NewItemState.description, F.text)
async def new_item_description(message: Message, state: FSMContext) -> None:
     await state.update_data(description=message.text)
     await state.set_state(NewItemState.price)
     await message.answer("Цена товара")
     

@admin_router.message(NewItemState.price, F.text)
async def new_item_price(message: Message, state: FSMContext) -> None:
     if message.text.isdigit() is False:
          return await message.answer("Нужно число!")
     
     await state.update_data(price=int(message.text))
     await state.set_state(NewItemState.image) 
     await message.answer("Картинка товара")
     
     
@admin_router.message(NewItemState.image, F.text)
@inject
async def new_item_photo(
     message: Message, 
     state: FSMContext,
     session: FromDishka[AsyncSession],
     service: FromDishka[AdminService]
) -> None:
     await state.update_data(image=message.text)
     
     result, state_del = await service.new_item(
          session=session,
          data=await state.get_data()
     )
     if state_del is True:
          await state.clear()
     await message.answer(result)
     
  
         
@admin_router.message(Command("new_item_doc"))
async def new_item_doc(
     message: Message,
     state: FSMContext
) -> None:
     await state.clear()
     await state.set_state(NewItemDocState.document)
     await message.answer("Отправьте документ с новыми товарами")
     
     
@admin_router.message(NewItemDocState.document, F.document)
@inject
async def new_item_doc_document(
     message: Message,
     state: FSMContext,
     session: FromDishka[AsyncSession],
     service: FromDishka[AdminService]
) -> None:
     ...
     
     

@admin_router.message(Command("delete_item"))
@inject
async def delete_item(
     message: Message,
     command: CommandObject,
     session: FromDishka[AsyncSession],
     service: FromDishka[AdminService],
) -> Optional[SendMessage]:
     if command.args is None:
          return await message.answer("Пример использования: /delete_item item_id")
     
     result = await service.delete_item(
          session=session,
          item_id=command.args
     )
     await message.answer(result)
    
     
     
@admin_router.message(Command("get_item"))
@inject
async def get_items(
     message: Message,
     command: CommandObject,
     session: FromDishka[AsyncSession],
     service: FromDishka[AdminService],
) -> Optional[SendMessage]:
     if command.args is None:
          return await message.answer("Пример использования: /get_item item_id или /get_item all")
     
     result = await service.get_items(
          session=session,
          item=command.args
     )
     if isinstance(result, str):
          return await message.answer(result)
     
     await message.answer_photo(
          photo=result[1],
          reply_markup=result[0]
     )
         
     
     
@admin_router.message(Command("new_admin"))
@inject
async def new_admin(
     message: Message,
     command: CommandObject,
     session: FromDishka[AsyncSession],
     service: FromDishka[AdminService],
) -> Optional[SendMessage]:
     if command.args is None:
          return await message.answer("Использование команды: /new_admin user_id")
     
     result = await service.new_admin(
          session=session,
          new_admin_id=command.args
     )
     await message.answer(result)
     
     
     
@admin_router.message(Command("admins"))
@inject
async def admins(
     message: Message,
     session: FromDishka[AsyncSession],
     service: FromDishka[AdminService]
) -> None:
     ...