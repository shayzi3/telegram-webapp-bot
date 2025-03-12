from datetime import datetime
from typing import Any, List, Generic, TypeVar

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import BigInteger, ForeignKey, Table, Column, func

from schemas import UserModel, ItemModel
     


M = TypeVar("M")



class Base(AsyncAttrs, DeclarativeBase, Generic[M]):
     __pydantic_model__ = Any
     
     def to_pydantic(self) -> M:
          return self.__pydantic_model__(**self.__dict__)



association_table = Table(
    "association_table",
    Base.metadata,
    Column("users", ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("items", ForeignKey("items.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)


class User(Base[UserModel]):
     __tablename__ = 'users'
     __pydantic_model__ = UserModel
     
     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     name: Mapped[str] = mapped_column()
     cash: Mapped[int] = mapped_column(BigInteger, default=0)
     is_admin: Mapped[bool] = mapped_column(default=False)
     created_at: Mapped[datetime] = mapped_column(server_default=func.now())
     
     basket: Mapped[List["Item"]] = relationship(
          back_populates="users", 
          lazy="joined",
          secondary=association_table,
          cascade="all, delete"
     )

     
     
     
class Item(Base[ItemModel]):
     __tablename__ = "items"
     __pydantic_model__ = ItemModel
     
     id: Mapped[str] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column()
     description: Mapped[str] = mapped_column()
     price: Mapped[int] = mapped_column(BigInteger)
     image: Mapped[str] = mapped_column()
     
     users: Mapped[List["User"]] = relationship(
          back_populates="basket", 
          lazy="joined",
          secondary=association_table,
          passive_deletes=True
     ) 