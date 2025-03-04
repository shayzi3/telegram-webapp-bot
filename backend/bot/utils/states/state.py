from aiogram.fsm.state import State, StatesGroup



class NewItemState(StatesGroup):
     name = State()
     description = State()
     price = State()
     image = State()