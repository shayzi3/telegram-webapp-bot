import json

from pydantic import BaseModel, field_validator
from datetime import datetime

from integration.redis import RedisManager



class UserModel(BaseModel, RedisManager["UserModel"]):
     id: int
     name: str
     cash: int
     is_admin: bool
     created_at: datetime
     basket: list        # list[Item]
     
     
     @field_validator("basket")
     @classmethod
     def basket_validate(cls, basket: list) -> list["ItemModel"]:
          if basket:
               basket = [item.to_pydantic() for item in basket if not isinstance(item, BaseModel)]
          return basket
     
     
     @property
     def redis_key(self) -> str:
          return f"user:{self.id}"
     
     
     @property
     def where(self) -> dict[str, str]:
          return {"id": self.id}
     
     
     def to_redis(self):
          self.created_at = self.created_at.timestamp()
          self.basket = [item.to_redis() for item in self.basket]
          return json.dumps(self.__dict__)
     
     
     @classmethod
     def from_redis(cls, model: str) -> "UserModel":
          decode_model = json.loads(model)
          
          decode_model["created_at"] = datetime.fromtimestamp(decode_model["created_at"])
          decode_model["basket"] = [ItemModel.from_redis(item) for item in decode_model["basket"]]
          return cls(**decode_model)
     
     
     
     
     
class ItemModel(BaseModel, RedisManager["ItemModel"]):
     id: str
     name: str
     description: str
     price: int
     image: str
     
     
     @property
     def redis_key(self) -> str:
          return f"item:{self.id}"
     
     
     @property
     def where(self) -> str:
          return {"id": self.id}