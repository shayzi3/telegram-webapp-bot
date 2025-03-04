import json

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Generic, TypeVar
from redis.asyncio import Redis
from datetime import datetime

from core import settings
        
        
        
M = TypeVar("M")

  
    
@asynccontextmanager
async def get_redis_session() -> AsyncGenerator[Redis, None]:   
     async with Redis(port=settings.redis_port, host=settings.redis_host) as redis:
          try:
               yield redis
          finally:
               await redis.close()
               
               
               
               
class RedisConverter(Generic[M]):
     
     @classmethod
     def __datetime_key(cls) -> list[str]:
          date = []
          for key, value in cls.__annotations__.items():
               if issubclass(value, datetime):
                    date.append(key)
          return date
     
     
     def to_redis(self) -> str:
          for date_key in self.__datetime_key():
               self.__dict__[date_key] = self.__dict__[date_key].timestamp()
          return json.dumps(self.__dict__)
     
     
     @classmethod
     def from_redis(cls, dump_model: str) -> M:
          model = json.loads(dump_model)
          
          for date_key in cls.__datetime_key():
               model[date_key] = datetime.fromtimestamp(model[date_key])
          return cls(**model)
     
     
     @classmethod
     async def get_from_redis(cls, key: str) -> M | None:
          async with get_redis_session() as redis:
               value = await redis.get(key)
               
               if value is None:
                    return None
          return cls.from_redis(value) 
     
     
     async def write_in_redis(self, expire: int) -> None:
          async with get_redis_session() as redis:
               await redis.set(
                    name=self.redis_key,
                    value=self.to_redis(),
                    ex=expire
               )