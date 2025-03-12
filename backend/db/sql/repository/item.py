from typing import Optional
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.sql.models import Item
from schemas import ItemModel
from .repository import Repository


class ItemRepository(Repository[ItemModel]):
     model = Item
     
     
     @classmethod
     async def get_count_items(
          cls,
          session: AsyncSession
     ) -> int:
          logger.info("SELECT COUNT FOR items")
          
          sttm = select(cls.model)
          response = await session.execute(sttm)
          result = response.unique() 
          
          return len(result.all())
     
     
     @classmethod
     async def limit_item(
          cls,
          session: AsyncSession,
          offset: int,
          limit: int,
          write_in_redis: bool = True,
          redis_get_value: Optional[str] = None
     ) -> Optional[ItemModel]:
          pydantic_model = cls.model.__pydantic_model__
          if redis_get_value is not None:
               value = await pydantic_model.get_from_redis(redis_get_value)
               if value is not None:
                    return value
          
          logger.info(f"SELECT DATA FROM items offset: {offset}; limit: {limit}")
          sttm = select(cls.model).offset(offset).limit(limit)
          response = await session.execute(sttm)
          scalar = response.scalar()
          
          if scalar is None:
               return None
          
          to_model = pydantic_model(**scalar.__dict__)
          if write_in_redis is True:
               await to_model.offset_write(offset=offset, limit=limit)
          return to_model