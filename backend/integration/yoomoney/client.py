from typing import Any
from aiogram import Bot
from aiogram.types import Message
from httpx import AsyncClient
from loguru import logger

from bot.utils.inline_buttons import url_button_builder
from .schema import YoomoneyResponse, PaymentType
from core import settings



class YoomoneyManager:
     
     async def payment_link(
          self,
          payment_type: PaymentType,
          money: int,
          label: str
     ) -> str:
          """
          payment_type:
               PC — оплата из кошелька ЮMoney
               AC — с банковской карты
          """
          if money <= 1:
               raise ValueError("money more than 1")
          
          if len(label) > 64:
               raise ValueError("label less or equal 64")
          
          body = {
               "receiver": settings.yoomoney_receiver,
               "quickpay-form": "button",
               "paymentType": payment_type,
               "sum": money,
               "label": label
          }
          url = "https://yoomoney.ru/quickpay/confirm?"
          for key, value in body.items():
               url += f"&{key}={value}"
          
          async with AsyncClient() as client:
               response = await client.post(url)
               
          logger.info(f"GENERATE PAYMENT LINK. LABEL: {label}")
          return response.text.split()[-1] # returns redirect url for pay
     
     
     async def bg_generate_payment(
          self, 
          user_message: Message, 
          bot_message: Message,
          payment_type: PaymentType,
          money: int,
          label: str
     ) -> None:
          link = await self.payment_link(payment_type, money, label)
          await bot_message.delete() # Удаляю сообщение `Ссылка генерируется...`
          
          await user_message.answer(
               text=f"Твоя ссылка для оплаты.",
               reply_markup=url_button_builder(text="Pay", url=link)
          )
          
          
     async def on_success(self, response: YoomoneyResponse, bot: Bot) -> Any:
          logger.info(f"SUCCESS PAYMENT. OPERATION_ID: {response.operation_id}")
          
          return await bot.send_message(
               chat_id=int(response.label),
               text=f"{response.withdraw_amount} отправлены успешно! \nOperation: {response.operation_label}"
          )
     

yoomoney_client = YoomoneyManager()
     