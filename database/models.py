import asyncio
import random

from string import ascii_letters
from typing import Annotated, Optional, Text

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy import BigInteger


# Users
UtypeID = Annotated[int, mapped_column(BigInteger, primary_key=True)]
UtypeSTR = Annotated[str, mapped_column()]
UtypeCASH = Annotated[int, mapped_column(BigInteger)]
GtypeGLOBAL = Annotated[Text, mapped_column()]


# Orders
OtypeID = Annotated[Text, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
     __tablename__ = 'user'
     
     id: Mapped[Optional[UtypeID]]
     name: Mapped[Optional[UtypeSTR]]
     basket: Mapped[Optional[GtypeGLOBAL]]
     cash: Mapped[Optional[UtypeCASH]]
     location: Mapped[Optional[UtypeSTR]] # '44.444 44.444'
     my_order: Mapped[Optional[GtypeGLOBAL]]
     surname: Mapped[Optional[UtypeSTR]]
     password: Mapped[Optional[GtypeGLOBAL]]
     
     
class Orders(Base):
     __tablename__ = 'order'   # table for admins
     
     id: Mapped[Optional[OtypeID]]   # id admins, who accept order. list[int] 
     orders: Mapped[Optional[GtypeGLOBAL]]  # orders. dict['id_buyer': (name_buyer, list[order])]
     
     
class Shop(Base):
     __tablename__ = 'shop'   # its table use only webApp
     
     id: Mapped[Optional[UtypeID]]
     password: Mapped[Optional[GtypeGLOBAL]]
     items: Mapped[Optional[GtypeGLOBAL]]  
     



class CreateAsyncSessions:
     __path = 'data/my.db'
     
     eng = create_async_engine(f'sqlite+aiosqlite:///{__path}', echo=True)
     session = async_sessionmaker(eng)
     
     
class MyTable(CreateAsyncSessions):
     
     @classmethod
     async def create_tables(cls) -> None:
          async with cls.eng.begin() as begin:
               await begin.run_sync(Base.metadata.create_all)
          
               
     @classmethod
     async def drop_tables(cls) -> None:
          async with cls.eng.begin() as begin:
               await begin.run_sync(Base.metadata.drop_all)
               
               
     @classmethod
     async def generate_password_user(cls) -> str:
          len_password = random.choice([i for i in range(15, 26)])
          data = ascii_letters + ''.join([str(i) for i in range(1, 10)])
          
          password = ''
          for _ in range(len_password):
               password += random.choice(data)
               
          return password
     
               
my_ = MyTable()
# asyncio.run(my_.drop_tables())
# asyncio.run(my_.create_tables())