
from fastapi import APIRouter

from schemas import ItemModel


item_router = APIRouter(prefix="/api/v1/item", tags=["Item"])



@item_router.get(path="/")
async def item_get() -> list[ItemModel]:
     """get data from db with offset"""