from pydantic import BaseModel
from datetime import datetime as time
from typing import Literal


PaymentType = Literal["AC", "PC"]
NotificationType = Literal["p2p-incoming", "card-incoming"]


class YoomoneyResponse(BaseModel):
     notification_type: NotificationType
     amount: float
     operation_id: str
     operation_label: str
     withdraw_amount: float
     currency: str
     datetime: time
     label: str
     
          
     """
     notification_type:
          p2p-incoming: Деньги отправлены с yoomoney
          card-incoming: Деньги отправлены с карты
     
     amount:
          Деньги, которые были получены
          
     operation_id:
          Идентификатор операции в истории кошелька
          
     operation_label:
          ID операции
          
     withdraw_amount:
          Сумма, которую сняли у отправителя
     
     сurrency:
          Код валюты
               643 - рубль
          
     datetime:
          Время совершения перевода
          
     label:
          Полезная информация платежа, отправленная вами же
     """