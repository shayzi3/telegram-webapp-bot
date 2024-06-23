
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router

from bot.utils.inline_buttons import start_buttons


router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
     text = 'Приветствую тебя в онлайн кафе! Чтобы сделать заказ ты должен зарегестрироваться.'
     
     await message.answer(text, reply_markup=start_buttons.start_btn_register)