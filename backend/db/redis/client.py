import json

from typing import Optional
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Generic, TypeVar
from redis.asyncio import Redis

from core import settings
from logs import logger
        
        
        
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
     async def get_from_redis(cls, key: str) -> Optional[M]:
          logger.redis.info(f"GET VALUE FROM REDIS {key}")
          
          async with get_redis_session() as redis:
               value = await redis.get(key)
               
               if value is None:
                    return None
          return cls.from_redis(value)

     
     async def write_in_redis(self) -> None:
          logger.redis.info(f"WRITE VALUE IN REDIS {self.redis_key}")
          
          async with get_redis_session() as session:
               await session.set(
                    name=self.redis_key,
                    value=self.to_redis(),
                    ex=self.__redis_expire__
               )
             
     @classmethod  
     async def delete_from_redis(cls, *keys) -> None:
          logger.redis.info(f"DELETE VALUE IN REDIS {keys}")
          
          async with get_redis_session() as session:
               await session.delete(*keys)
               

     async def offset_write(self, offset: int, limit: int) -> None:
          logger.redis.info(f"WRITE OFFSET VALUE IN REDIS off={offset}lim={limit}")
          
          async with get_redis_session() as session:
               await session.set(
                    name=f"item:off={offset}lim={limit}",
                    value=self.to_redis(),
                    ex=self.__offset_redis_expire__
               )