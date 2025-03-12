from db.sql.models import User
from schemas import UserModel
from .repository import Repository


class UserRepository(Repository[UserModel]):
     model = User