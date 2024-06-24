
from json import loads, dumps
from typing import Any
from sqlalchemy import select, insert, update
from database.models import Users, CreateAsyncSessions, my_


class UsersORM(CreateAsyncSessions):
     
     @classmethod
     async def insert_data(cls, user_id: int, surname: str, location: list[int], name: str) -> None:
          loc = f'{location[0]} {location[1]}'
          
          async with cls.session.begin() as session:
               sttm = (
                    insert(Users).
                    values(
                         id=user_id,
                         name=name,
                         cash=100,
                         location=loc,
                         surname=surname,
                         my_order=dumps([]),
                         basket=dumps([]),
                         password=await my_.generate_password_user()
                    )
               )
               await session.execute(sttm)
               
               
     @classmethod
     async def user_in_database(cls, user_id: int) -> bool:
          async with cls.session() as session:
               sttm = select(Users.id).where(Users.id == user_id)
               
               response = await session.execute(sttm)
               if not response.scalar():
                    return False
               return True
          
     
     @classmethod
     async def take_id_password(cls, user_id: int) -> tuple[Any]:
          async with cls.session() as session:
               sttm = select(Users.id, Users.password).where(Users.id == user_id)
               
               response = await session.execute(sttm)
          return response.fetchone()
               
               
user_orm = UsersORM()
               