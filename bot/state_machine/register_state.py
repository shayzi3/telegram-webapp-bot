from string import ascii_letters

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.utils.states.register_fsm import Register
from bot.utils.keyboard_buttons import register_state_loc as location_


router = Router()


class ValidNameSurname:
     
     @staticmethod
     async def validData(nameSurname: list[str]) -> int | bool:
          if len(nameSurname) < 2:
               return 2
          
          if not isinstance(nameSurname[0], str) or not isinstance(nameSurname[1], str):
               return 0
          
          toge = nameSurname[0].lower() + nameSurname[1].lower()
          if len(toge.strip(ascii_letters)) != 0:
               print(toge.strip(ascii_letters))
               return 1
          
          return True
          
          
          
          

@router.message(Register.name_surname, F.text)
async def name_surname(message: Message, state: FSMContext) -> None:
     valid = ValidNameSurname()
     check = await valid.validData(nameSurname=message.text.split())
     
     if check == 2 or check == 0 or check == 1:
          await message.answer('Введен неправильный формат. Пример: Иван Иванов или Иван Иванов Иванович')
          return
          
     await state.update_data(name_surname = message.text)
     await state.set_state(Register.location)
     await message.answer('Теперь отправьте геолокацию', reply_markup=location_.location_btn)
     
     
@router.message(Register.location, F.location)
async def location(message: Message, state: FSMContext) -> None:
     await state.update_data(location = message.location)    
     
     data = await state.get_data()
     
     await message.answer('Геопозиция добавлена. Регистрация завершена. 🚀', reply_markup=ReplyKeyboardRemove())
     await message.answer_location(
          latitude=data['location'].latitude, 
          longitude=data['location'].longitude
     )
     await state.clear()
     
     
          