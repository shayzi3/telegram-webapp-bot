
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


location_btn = ReplyKeyboardMarkup(
     keyboard=[
          [
               KeyboardButton(text='📌 Геопозиция', request_location=True)
          ]
     ],
     one_time_keyboard=True,
     resize_keyboard=True
)