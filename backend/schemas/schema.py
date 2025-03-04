from pydantic import BaseModel, field_validator
from datetime import datetime

from integration.redis import RedisConverter






class UserModel(BaseModel, RedisConverter["UserModel"]):
     id: int
     name: str
     cash: int
     is_admin: bool
     created_at: datetime
     basket: list       # list[Item]
     
     @field_validator("basket")
     @classmethod
     def basket_validate(cls, basket: list) -> list["ItemModel"]:
          if basket:
               basket = [item.to_pydantic() for item in basket]
          return basket
     
     
     @property
     def redis_key(self) -> str:
          return f"user:{self.id}"
     
     
     
     
class ItemModel(BaseModel, RedisConverter["ItemModel"]):
     id: int
     name: str
     description: str
     price: int
     image: str
     
     
     @property
     def redis_key(self) -> str:
          return f"item:{self.id}"