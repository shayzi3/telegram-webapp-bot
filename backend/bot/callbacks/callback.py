from aiogram.types.callback_query import CallbackQuery
from aiogram import Router, F



callback_router = Router(name="callback_royter")


@callback_router.callback_query(F.data == "msg_delete")
async def message_delete(query: CallbackQuery) -> None:
     await query.message.delete()
     await query.answer()
     
     
@callback_router.callback_query(F.data == "empty")
async def empty_callback(query: CallbackQuery) -> None:
     await query.answer(text="Эта кнопка ничего не делает:/")