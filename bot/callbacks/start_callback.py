
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.utils.inline_buttons.start_buttons import Reg
from bot.utils.states.register_fsm import Register


router = Router()


@router.callback_query(Reg.filter())
async def register(query: CallbackQuery, state: FSMContext) -> None:
     await state.set_state(Register.name_surname)
     await query.message.answer('Отправьте своё имя и фамилию.')
     
     await query.answer()
     