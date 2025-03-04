from typing import Any, Generic, TypeVar

from abc import ABC, abstractmethod
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession



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
     async def update(self, session, where: dict[str, Any], **extras) -> None:
          ...
          
          
     @abstractmethod  
     async def delete(self, session, where: dict[str, Any]) -> None:
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
          
          
     @classmethod
     async def read(
          cls, 
          session: AsyncSession, 
          write_in_redis: bool = True,
          **extras
     ) -> Model | None:
          """extras - where value"""
          
          sttm = select(cls.model).filter_by(**extras)
          result = await session.execute(sttm)
          scalar = result.scalar()
               
          if not scalar:
               return None
          
          model = cls.model.__pydantic_model__(**scalar.__dict__)
          if write_in_redis is True:
               await model.write_in_redis(expire=200)
          return model
          
          
     @classmethod
     async def update(
          cls, 
          session: AsyncSession, 
          where: dict[str, Any],
          clear_in_redis: bool = True,
          **extras
     ) -> None:
          """extras - values while need update"""
          sttm = (
               update(cls.model).filter_by(**where).values(**extras)
          )
          await session.execute(sttm)
          await session.commit()
          
          if clear_in_redis:
               ...
          
     
     
     @classmethod
     async def delete(
          cls, 
          session: AsyncSession, 
          where: dict[str, Any],
          clear_in_redis: bool = True
     ) -> None:
          sttm = (
               delete(cls.model).filter_by(**where)
          )
          await session.execute(sttm)
          await session.commit()
          
          if clear_in_redis:
               ...