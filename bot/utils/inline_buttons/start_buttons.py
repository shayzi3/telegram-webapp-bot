
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

# class Reg(CallbackData, prefix='register'):
#      action: bool
     

start_btn_register = InlineKeyboardMarkup(
     inline_keyboard=[
          [
               InlineKeyboardButton(text='🪪 Зарегистрироваться', callback_data='reg')
          ]
     ]
)