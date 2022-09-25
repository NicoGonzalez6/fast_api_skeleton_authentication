
from typing import List, Optional
from pydantic import BaseModel
from schemas.user_schema import ShowUserNews


class Game_News_Schema(BaseModel):
    title: str
    span: Optional[str]
    subtitle: Optional[str]
    link: str
    image: str
    comments: str
    page: Optional[str]

    class Config:
        orm_mode = True


class Show_Games_schema(Game_News_Schema):
    id: int
    title: str
    span: Optional[str]
    subtitle: Optional[str]
    link: str
    image: str
    comments: str
    page: Optional[str]
    creator: ShowUserNews

    class Config:
        orm_mode = True


class Response_User_Game_news(BaseModel):
    name: str
    email: str
    news: List[Game_News_Schema]

    class Config:
        orm_mode = True
