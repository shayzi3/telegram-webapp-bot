from sqlalchemy.ext.asyncio import AsyncSession

from db.sql.repository import UserRepository
from schemas import UserModel



class UserService:
     
     
     async def start(
          self, 
          id: int,
          name: str,
          session: AsyncSession
     ) -> str:
          user = await UserRepository.read(
               id=id,
               write_in_redis=True,
               redis_get_value=f"user:{id}",
               session=session
          )
          if user is None:
               await UserRepository.create(
                    id=id,
                    name=name,
                    session=session
               )
          return "Совершай покупки в WebApp приложении!"
               
               
async def get_user_service() -> UserService:
     return UserService()