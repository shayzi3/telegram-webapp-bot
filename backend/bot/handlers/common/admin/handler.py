from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from .service import AdminService
from bot.utils.states import NewItemState
from bot.midlewares import IsAdminMiddleware


admin_router = Router(name=__name__)
admin_router.message.middleware(IsAdminMiddleware())


@admin_router.message(Command("new_item"))
@inject
async def new_item(message: Message, state: FSMContext) -> None:
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
     service: FromDishka[AdminService]
) -> None:
     await state.update_data(image=message.text)
     
     response = await service.new_item(
          container=message.dishka,
          data=await state.get_data()
     )
     if response is False:
          return await message.answer("URL недействителен! Отправьте повторно")
     
     await state.clear()
     await message.answer("Новый предмет добавлен успешно!")
          

     
@admin_router.message(Command("new_admin"))
@inject
async def new_admin(
     message: Message,
     service: FromDishka[AdminService],
) -> None:
     ...