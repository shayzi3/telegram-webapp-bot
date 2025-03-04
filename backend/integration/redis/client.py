
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