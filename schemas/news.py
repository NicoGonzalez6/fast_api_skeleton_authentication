from typing import List, Optional
from pydantic import BaseModel
from schemas.user_schema import ShowUserNews


class news_schema(BaseModel):
    title: str
    subtitle: Optional[str]
    link: str
    image: str
    page: Optional[str]

    class Config:
        orm_mode = True


class response_news_schemna(BaseModel):
    id: int
    title: str
    subtitle: Optional[str]
    link: str
    image: str
    page: Optional[str]
    creator: ShowUserNews

    class Config:
        orm_mode = True
