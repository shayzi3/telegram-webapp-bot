from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


from bot.utils.filters.callback import ItemCallback, PaginatorCallback
from bot.utils.enums import PageMode
from schemas import ItemModel
from core import settings



delete_message = InlineKeyboardMarkup(
     inline_keyboard=[
          [
               InlineKeyboardButton(text="Удалить сообщение", callback_data="msg_delete")
          ]
     ]
)



def url_button_builder(text: str, url: str) -> InlineKeyboardMarkup:
     keyboard = InlineKeyboardBuilder()
     
     keyboard.add(
          InlineKeyboardButton(text=text, url=url)
     )
     return keyboard.as_markup()




def webapp_button_builder(user_id: int) -> InlineKeyboardMarkup:
     keyboard = InlineKeyboardBuilder()
     
     keyboard.add(
          InlineKeyboardButton(
               text="Tasty's Shop",
               web_app=WebAppInfo(url=settings.webapp_url + f"/{user_id}")
          )
     )
     return keyboard.as_markup()



def item_page_builder(
     data: ItemModel, 
     mode: PageMode,
     data_len: int = 0,
     offset: int = 0,
     limit: int = 1,
) -> InlineKeyboardMarkup:
     keyboard = InlineKeyboardBuilder()
     
     keyboard.add(
          InlineKeyboardButton(
               text="Удалить",
               callback_data=ItemCallback(id=data.id, filter_mode="delete").pack()
          ),
          InlineKeyboardButton(
               text="Изменить",
               callback_data=ItemCallback(id=data.id, filter_mode="change").pack()
          ),
          InlineKeyboardButton(
               text="Просмотреть информацию",
               callback_data=ItemCallback(id=data.id, filter_mode="info").pack()
          )
     )
     keyboard.adjust(2, 1)
     
     if mode == PageMode.ALL:
          keyboard.add(
               InlineKeyboardButton(
                    text="<",
                    callback_data=PaginatorCallback(
                         limit=limit, 
                         offset=offset, 
                         paginate_mode="left",
                         data_len=data_len
                    ).pack()
               ),
               InlineKeyboardButton(
                    text=">",
                    callback_data=PaginatorCallback(
                         limit=limit,
                         offset=offset,
                         paginate_mode="right",
                         data_len=data_len
                    ).pack()
               ),
               InlineKeyboardButton(
                    text=f"{offset + 1}/{data_len}",
                    callback_data=PaginatorCallback(
                         limit=limit,
                         offset=offset,
                         paginate_mode="count",
                         data_len=data_len
                    ).pack()
               )
          )
          keyboard.adjust(2, 1, 2, 1)
     return keyboard.as_markup()