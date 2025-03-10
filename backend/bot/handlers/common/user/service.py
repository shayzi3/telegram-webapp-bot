from sqlalchemy.ext.asyncio import AsyncSession
from dishka.async_container import AsyncContainer

from db.repository import UserRepository
from schemas import UserModel



class UserService:
     
     
     async def start(
          self, 
          id: int,
          name: str,
          session: AsyncSession
     ) -> str:
          user = await UserModel.get_from_redis(f"user:{id}")
          if user is None:
               user = await UserRepository.read(
                    id=id,
                    write_in_redis=True,
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