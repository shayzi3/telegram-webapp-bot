from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from core import settings



def url_button_builder(text: str, url: str) -> InlineKeyboardMarkup:
     build = InlineKeyboardBuilder()
     
     build.add(
          InlineKeyboardButton(text=text, url=url)
     )
     return build.as_markup()



def webapp_button_builder(user_id: int) -> InlineKeyboardMarkup:
     keyboard = InlineKeyboardBuilder()
     
     keyboard.add(
          InlineKeyboardButton(
               text="Tasty's Shop",
               web_app=WebAppInfo(url=settings.webapp_url + f"/{user_id}")
          )
     )
     return keyboard.as_markup()



