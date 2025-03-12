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
          write_in_redis: bool = True
     ) -> Optional[ItemModel]:
          logger.info(f"SELECT DATA FROM items offset: {offset}; limit: {limit}")
          
          sttm = select(cls.model).offset(offset).limit(limit)
          response = await session.execute(sttm)
          scalar = response.scalar()
          
          if scalar is None:
               return None
          
          model = cls.model.__pydantic_model__(**scalar.__dict__)
          if write_in_redis is True:
               await model.offset_write(offset=offset, limit=limit)
          return model