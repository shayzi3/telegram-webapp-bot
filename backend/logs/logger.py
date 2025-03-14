import logging

from datetime import datetime



class BaseLogger(logging.Logger):
     def __init__(self, name: str, path: str):
          super().__init__(name=name)
          
          self.setLevel(logging.INFO)
          
          logger_handler = logging.FileHandler(
               filename=path + datetime.now().strftime("%Y-%m-%d") + ".txt",
               mode="a"
          )
          logger_format = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
          
          logger_handler.setFormatter(logger_format)
          self.addHandler(logger_handler)



class Logger:
     
     @property
     def app(self) -> BaseLogger:
          return BaseLogger(
               name="app",
               path="backend/logs/app/logs/"
          )
          
          
     @property
     def bot(self) -> BaseLogger:
          return BaseLogger(
               name="bot",
               path="backend/logs/bot/logs/"
          )
          
          
     @property
     def sql(self) -> BaseLogger:
          return BaseLogger(
               name="sql",
               path="backend/logs/sql/logs/"
          )
          
          
     @property
     def redis(self) -> BaseLogger:
          return BaseLogger(
               name="redis",
               path="backend/logs/redis/logs/"
          )
          
          
     @property
     def yoomoney(self) -> BaseLogger:
          return BaseLogger(
               name="yoomoney",
               path="backend/logs/yoomoney/logs/"
          )
     
     
     
logger = Logger()