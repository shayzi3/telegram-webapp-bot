from sqlalchemy.ext.asyncio import AsyncSession
from dishka.async_container import AsyncContainer

from db.repository import UserRepository
from schemas import UserModel



class UserService:
     def __init__(self, user_repository: UserRepository):
          self.user_repository = user_repository
     
     
     async def start(
          self, 
          id: int,
          name: str,
          container: AsyncContainer
     ) -> None:
          user = await UserModel.get_from_redis(f"user:{id}")
          if user is None:
               session = await container.get(AsyncSession)
               user = await self.user_repository.read(
                    id=id,
                    write_in_redis=True,
                    session=session
               )
               if user is None:
                    await self.user_repository.create(
                         id=id,
                         name=name,
                         session=session
                    )
          return None
               
               
async def get_user_service() -> UserService:
     return UserService(
          user_repository=UserRepository()
     )