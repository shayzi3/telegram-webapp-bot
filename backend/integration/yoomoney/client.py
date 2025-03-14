from aiogram.types import Message
from httpx import AsyncClient
from aiogram import Bot

from bot.utils.inline_buttons import url_button_builder
from core import settings
from logs import logger
from .schema import YoomoneyResponse, PaymentType




class YoomoneyManager:
     
     async def _payment_link(
          self,
          payment_type: PaymentType,
          money: int,
          label: str
     ) -> str:
          """
          payment_type:
               PC — оплата из кошелька ЮMoney
               AC — с банковской карты
               
          money > 1
          label <= 64
          """
          logger.yoomoney.info(f"GENEATE NEW LINK. LABEL: {label} MONEY: {money}")
          
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
          return response.text.split()[-1] # returns redirect url for pay
     
     
     async def bg_generate_payment(
          self, 
          user_message: Message, 
          bot_message: Message,
          payment_type: PaymentType,
          money: int,
          label: str
     ) -> None:
          link = await self._payment_link(payment_type, money, label)
          await bot_message.delete() # Delete message `Ссылка генерируется...`
          
          await user_message.answer(
               text=f"Твоя ссылка для оплаты.",
               reply_markup=url_button_builder(text="Pay", url=link)
          )
          
          
     async def on_success(self, response: YoomoneyResponse, bot: Bot) -> None:
          logger.yoomoney.info(f"SUCCESS PAYMENT. OPERATION_ID: {response.operation_id} LABEL: {response.label}")
          
          await bot.send_message(
               chat_id=int(response.label),
               text=f"{response.withdraw_amount} отправлены успешно! \nOperation: {response.operation_label}"
          )
     

yoomoney_client = YoomoneyManager()
     