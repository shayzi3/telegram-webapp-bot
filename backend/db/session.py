from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
from core import settings


class Session:
     eng = create_async_engine(settings.postgres, echo=False)
     async_session = async_sessionmaker(eng)