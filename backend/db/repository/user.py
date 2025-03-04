from db.models import User
from .repository import Repository
from schemas import UserModel



class UserRepository(Repository[UserModel]):
     model = User