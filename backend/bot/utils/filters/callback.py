from aiogram.filters.callback_data import CallbackData



class ItemCallback(CallbackData, prefix="item"):
     id: str
     filter_mode: str
     
     
     
class PaginatorCallback(CallbackData, prefix="paginator"):
     limit: int = 1
     offset: int
     paginate_mode: str
     data_len: int