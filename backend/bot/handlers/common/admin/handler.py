from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.aiogram import inject
from dishka import FromDishka

from .service import AdminService
from bot.utils.states import NewItemState, NewItemDocState
from bot.midlewares import IsAdminMiddleware


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
     session: FromDishka[AsyncSession],
     service: FromDishka[AdminService],
     item_id: str | None = None
) -> None:
     if item_id is None:
          return await message.answer("Пример использования: /delete_item item_id")
     
     result = await service.delete_item(
          session=session,
          item_id=item_id
     )
     await message.answer(result)
    
     
@admin_router.message(Command("get_item"))
@inject
async def get_items(
     message: Message,
     session: FromDishka[AsyncSession],
     service: FromDishka[AdminService],
     flag: str | None = None
) -> None:
     """flag - id item or `all`"""
          

     
@admin_router.message(Command("new_admin"))
@inject
async def new_admin(
     message: Message,
     session: FromDishka[AsyncSession],
     service: FromDishka[AdminService],
     new_admin_id: str | None = None,
) -> None:
     if new_admin_id is None:
          return await message.answer("Использование команды: /new_admin user_id")
     
     result = await service.new_admin(
          session=session,
          new_admin_id=new_admin_id
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