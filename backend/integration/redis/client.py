import json

from loguru import logger
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Generic, TypeVar
from redis.asyncio import Redis

from core import settings
        
        
        
M = TypeVar("M")

  
    
@asynccontextmanager
async def get_redis_session() -> AsyncGenerator[Redis, None]:   
     async with Redis(port=settings.redis_port, host=settings.redis_host) as redis:
          try:
               yield redis
          finally:
               await redis.close()
               
             
               
               
class RedisManager(Generic[M]):
     
     def to_redis(self) -> str:
          return json.dumps(self.__dict__)
     
     
     @classmethod
     def from_redis(cls, model: str) -> M:
          decode_model = json.loads(model)
          return cls(**decode_model)

     
     @classmethod
     async def get_from_redis(cls, key: str) -> M | None:
          logger.info(f"GET VALUE FROM REDIS {key}")
          
          async with get_redis_session() as redis:
               value = await redis.get(key)
               
               if value is None:
                    return None
          return cls.from_redis(value)
     
     
     async def write_in_redis(self, expire: int) -> None:
          logger.debug(f"WRITE VALUE IN REDIS {self.redis_key}")
          
          async with get_redis_session() as redis:
               await redis.set(
                    name=self.redis_key,
                    value=self.to_redis(),
                    ex=expire
               )