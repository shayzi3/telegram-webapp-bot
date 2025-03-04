from pydantic_settings import BaseSettings, SettingsConfigDict




class Settings(BaseSettings):
     bot_token: str
     postgres: str
     webhook_url: str
     webapp_url: str
     yoomoney_secret: str
     aiogram_secret: str
     yoomoney_receiver: str
     admins: list[int]
     redis_port: int
     redis_host: str
     
     @property
     def yoomoney_webhook(self) -> str:
          return self.webhook_url + f"/api/v1/yoomoney_webhook?secret={self.yoomoney_secret}"
     
     @property
     def aiogram_webhook(self) -> str:
          return self.webhook_url + f"/api/v1/aiogram_webhook?secret={self.aiogram_secret}"
     
     model_config = SettingsConfigDict(env_file='backend/core/.env')
     
     
settings = Settings()