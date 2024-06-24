
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode

from database.queries.users import user_orm


router = Router()


@router.message(Command('me'))
async def me(message: Message) -> None:
     us_pass = await user_orm.take_id_password(user_id=message.from_user.id)
     
     text = f'Ваш ID: <b>{us_pass[0]}</b> \nВаш пароль: <b>{us_pass[1]}</b> \n\nЭти данные нужны чтобы зарегестрироваться в Mini App.'
     
     await message.answer(text, parse_mode=ParseMode.HTML)
     
     
