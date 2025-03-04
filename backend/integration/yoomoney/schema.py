from datetime import datetime as time
from dataclasses import dataclass, fields
from typing import Any, Literal


PaymentType = Literal["AC", "PC"]


@dataclass
class YoomoneyResponse:
     notification_type: str
     amount: float
     operation_id: str
     operation_label: str
     withdraw_amount: float
     currency: str
     datetime: str
     label: str
     
     def __post_init__(self) -> None:
          self.amount = float(self.amount)
          self.withdraw_amount = float(self.withdraw_amount)
          self.datetime = time.now().strftime("%b %d %Y %H:%M:%S")
          
          
     @classmethod
     def from_dict(cls, payload: dict[str, Any]) -> "YoomoneyResponse":
          data_fields = [field.name for field in fields(cls)]
          return cls(**{key: value for key, value in payload.items() if key in data_fields})
          
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