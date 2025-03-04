from pydantic import HttpUrl, BaseModel


class ValidateUrl(BaseModel):
     url: HttpUrl
     
