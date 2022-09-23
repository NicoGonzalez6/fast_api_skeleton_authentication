
from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class Response_User(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
