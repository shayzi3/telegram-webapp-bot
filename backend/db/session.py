from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core import settings


class Session:
     eng = create_async_engine(settings.postgres, echo=True)
     async_session = async_sessionmaker(eng)
