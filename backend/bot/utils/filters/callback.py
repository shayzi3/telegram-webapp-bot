from aiogram.filters.callback_data import CallbackData



class ItemCallback(CallbackData, prefix="item"):
     id: str
     filter_mode: str
     
     
     @property
     def redis_key(self) -> str:
          return f"item:{self.id}"
     
     
     
class PaginatorCallback(CallbackData, prefix="paginator"):
     limit: int = 1
     offset: int
     paginate_mode: str
     data_len: int
     
     
     @property
     def redis_key_right(self) -> str:
          return f"item:off={self.offset + 1}lim={self.limit}"
     
     
     @property
     def redis_key_left(self) -> str:
          return f"item:off={self.offset - 1}lim={self.limit}"