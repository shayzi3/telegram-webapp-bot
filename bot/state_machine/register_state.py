
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.utils.states.register_fsm import Register
from bot.utils.keyboard_buttons import register_state_loc as location_
from database.queries.users import user_orm


router = Router()


class ValidNameSurname:
     letters = 'йцукенгшщзхъфывапролджэячсмитьбю' + 'qwertyuiopasdfghjklzxcvbnm'
     
     @classmethod
     async def validData(cls, nameSurname: list[str]) -> int | None:
          if len(nameSurname) < 2:
               return True
          
          elif not isinstance(nameSurname[0], str) or not isinstance(nameSurname[1], str):
               return True
          
          toge = nameSurname[0].lower() + nameSurname[1].lower()
          if len(toge.strip(cls.letters)) != 0:
               return True
          
          

@router.message(Register.name_surname, F.text)
async def name_surname(message: Message, state: FSMContext) -> None:
     await state.update_data(name_surname = message.text)
     
     valid = ValidNameSurname()
     check = await valid.validData(nameSurname=message.text.split())
     
     if check:
          await message.answer('Введен неправильный формат. Пример: Иван Иванов или Иван Иванов Иванович')
     
     elif not check:          
          await state.set_state(Register.location)
          await message.answer('Теперь отправьте геолокацию', reply_markup=location_.location_btn)
          
          
     
     
@router.message(Register.location, F.location)
async def location(message: Message, state: FSMContext) -> None:
     await state.update_data(location = message.location)    
     
     data = await state.get_data()
     
     await message.answer('Геопозиция добавлена. 🚀 Регистрация завершена. /me команда чтобы продолжить работу', reply_markup=ReplyKeyboardRemove())
     
     await user_orm.insert_data(
          user_id=message.from_user.id,
          surname=data['name_surname'],
          location=[data['location'].latitude, data['location'].longitude],
          name=message.from_user.full_name
     )
     
     await state.clear()
     
     
          