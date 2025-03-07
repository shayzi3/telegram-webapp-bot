from aiogram.filters.callback_data import CallbackData


class ItemCallback(CallbackData, prefix="item", sep="~"):
     id: str
     name: str
     description: str
     price: int
     filter_mode: str
     
     
     @classmethod
     def from_model(cls, model: type, filter_mode: str) -> "ItemCallback":
          kwargs = {"filter_mode": filter_mode}
          for item, value in model.__dict__.items():
               if item in cls.__annotations__:
                    kwargs[item] = value
          return cls(**kwargs)
     
     
     @property
     def to_info(self) -> str:
          return f"ID: {self.id} \nNAME: {self.name} \nDESCRIPTION: {self.description} \nPRICE: {self.price}"
     
     
     
class PaginatorCallback(CallbackData, prefix="paginator"):
     limit: int = 1
     offset: int
     paginate_mode: str
     data_len: int