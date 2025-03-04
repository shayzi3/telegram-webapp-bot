from .repository import Repository
from schemas import ItemModel
from db.models import Item


class ItemRepository(Repository[ItemModel]):
     model = Item