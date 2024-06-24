
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.enums.parse_mode import ParseMode

from bot.utils.inline_buttons import start_buttons
from database.queries.users import user_orm


router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
     text = 'Приветствую тебя в онлайн кафе! Чтобы сделать заказ ты должен зарегестрироваться.'
     markup = start_buttons.start_btn_register
     
     register = await user_orm.user_in_database(user_id=message.from_user.id)
     if register:
          text, markup = f'Рад тебя видеть, <b>{message.from_user.full_name}</b>', None
     
     await message.answer(text, reply_markup=markup, parse_mode=ParseMode.HTML)