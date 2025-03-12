from aiogram.types.callback_query import CallbackQuery
from aiogram import Router, F



callback_router = Router(name="callback_router")


@callback_router.callback_query(F.data == "msg_delete")
async def message_delete(query: CallbackQuery) -> None:
     await query.message.delete()