from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
from core import settings


class Session:
     eng = create_async_engine(settings.postgres, echo=False)
     async_session = async_sessionmaker(eng)
     
     
@asynccontextmanager
async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
     async with Session.async_session() as session:
          try:
               yield session
          finally:
               await session.close()