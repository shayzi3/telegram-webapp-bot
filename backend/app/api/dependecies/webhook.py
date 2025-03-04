from fastapi import HTTPException, status
from core import settings


error = HTTPException(
     detail="Invalid secret!",
     status_code=status.HTTP_403_FORBIDDEN
)

async def secret_aiogram(secret: str) -> None:
     if secret != settings.aiogram_secret:
          raise error
          
          
async def secret_yoomoney(secret: str) -> None:
     if secret != settings.yoomoney_secret:
          raise error