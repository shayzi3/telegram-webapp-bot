
from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
     name_surname = State()
     location = State()