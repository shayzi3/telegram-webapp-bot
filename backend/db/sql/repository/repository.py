from typing import Any, Generic, TypeVar, Optional
from abc import ABC, abstractmethod
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.redis import RedisManager
from logs import logger




Model = TypeVar("Model")



class AbstractRepository(ABC):
     model = None
     
     
     @abstractmethod
     async def create(self, session, **extras) -> None:
          ...
          
          
     @abstractmethod
     async def read(self, session, **extras) -> Optional[Model]:
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
          logger.sql.info(f"INSERT data in {cls.model.__tablename__}: {extras}")
          
          sttm = (
               insert(cls.model).
               values(**extras)
          )
          await session.execute(sttm)
          await session.commit()        
          
          
          
     @classmethod
     async def read(
          cls, 
          session: AsyncSession, 
          write_in_redis: bool = True,
          redis_get_value: Optional[str] = None,
          *args,
          **extras
     ) -> Optional[Model | list[Any]]:
          """extras - where value"""
          pydantic_model = cls.model.__pydantic_model__
          if redis_get_value is not None:
               value = await pydantic_model.get_from_redis(redis_get_value)
               if value is not None:
                    return value
          
          logger.sql.info(f"SELECT data FROM {cls.model.__tablename__}: {extras}")
          sttm = select(cls.model).filter_by(**extras)
          result = await session.execute(sttm)
          scalar = result.scalar()
               
          if not scalar:
               return None
          
          if args:
               return [scalar.__dict__.get(arg) for arg in args]
          
          to_model = pydantic_model(**scalar.__dict__)
          if write_in_redis is True:
               await to_model.write_in_redis()
          return to_model
          
          
     @classmethod
     async def update(
          cls, 
          session: AsyncSession, 
          where: dict[str, Any],
          delete_redis_values: list[str] = [],
          **extras
     ) -> None:
          """extras - values while need update"""
          logger.sql.info(f"UPDATE data in {cls.model.__tablename__} WHERE {where} VALUES {extras}")
          
          sttm = (
               update(cls.model).filter_by(**where).values(**extras).returning(cls.model.id)
          )
          await session.execute(sttm)
          await session.commit()
          
          if delete_redis_values:
               await RedisManager.delete_from_redis(*delete_redis_values)
          
     
     
     @classmethod
     async def delete(
          cls, 
          session: AsyncSession, 
          where: dict[str, Any],
          delete_redis_values: list[str] = []
     ) -> None:
          logger.sql.info(f"DELETE data in {cls.model.__tablename__} WHERE {where}")
          
          sttm = (
               delete(cls.model).filter_by(**where)
          )
          await session.execute(sttm)
          await session.commit()
          
          if delete_redis_values:
               await RedisManager.delete_from_redis(*delete_redis_values)