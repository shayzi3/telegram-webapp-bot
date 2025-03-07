from typing import Any, Generic, TypeVar
from loguru import logger

from abc import ABC, abstractmethod
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from integration.redis import RedisManager



Model = TypeVar("Model")



class AbstractRepository(ABC):
     model = None
     
     
     @abstractmethod
     async def create(self, session, **extras) -> None:
          ...
          
          
     @abstractmethod
     async def read(self, session, **extras) -> Model | None:
          ...
          
          
     @abstractmethod
     async def update(self, session, where, **extras) -> None:
          ...
          
          
     @abstractmethod  
     async def delete(self, session, where) -> None:
          ...
          
     
          
class Repository(Generic[Model], AbstractRepository):
     model = None
     
     
     @classmethod
     async def create(cls, session: AsyncSession, **extras) -> None:
          """extras - values"""
          sttm = (
               insert(cls.model).
               values(**extras)
          )
          await session.execute(sttm)
          await session.commit()        
          logger.debug(f"INSERT data in {cls.model.__tablename__}: {extras}")
          
          
     @classmethod
     async def read(
          cls, 
          session: AsyncSession, 
          write_in_redis: bool = True,
          *args,
          **extras
     ) -> Model | list[Any] | None:
          """extras - where value"""
          logger.info(f"SELECT data FROM {cls.model.__tablename__}: {extras}")
          
          sttm = select(cls.model).filter_by(**extras)
          result = await session.execute(sttm)
          scalar = result.scalar()
               
          if not scalar:
               return None
          
          if args:
               return [scalar.__dict__.get(arg) for arg in args]
          
          model = cls.model.__pydantic_model__(**scalar.__dict__)
          if write_in_redis is True:
               await model.write_in_redis()
          return model
          
          
     @classmethod
     async def update(
          cls, 
          session: AsyncSession, 
          where: dict[str, Any],
          delete_redis_values: list[str] = [],
          **extras
     ) -> None:
          """extras - values while need update"""
          sttm = (
               update(cls.model).filter_by(**where).values(**extras).returning(cls.model.id)
          )
          await session.execute(sttm)
          await session.commit()
          logger.debug(f"UPDATE data in {cls.model.__tablename__} WHERE {where} VALUES {extras}")
          
          if delete_redis_values:
               await RedisManager.delete_from_redis(*delete_redis_values)
          
     
     
     @classmethod
     async def delete(
          cls, 
          session: AsyncSession, 
          where: dict[str, Any],
          delete_redis_values: list[str] = []
     ) -> None:
          sttm = (
               delete(cls.model).filter_by(**where)
          )
          await session.execute(sttm)
          await session.commit()
          logger.debug(f"DELETE data in {cls.model.__tablename__} WHERE {where}")
          
          if delete_redis_values:
               await RedisManager.delete_from_redis(*delete_redis_values)