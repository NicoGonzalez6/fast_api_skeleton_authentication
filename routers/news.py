from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.db import get_db
from utils import oauth2
from services import news_services
from schemas.news import news_schema, response_news_schemna


router = APIRouter(
    prefix="/News",
    tags=["News"]
)


@router.get('/d_cuyo_news', status_code=status.HTTP_200_OK)
def GET_DCUYO_NEWS(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    return news_services.News_Services.Get_DC_NEWS()


@router.get('/tn_news', status_code=status.HTTP_200_OK)
def GET_TN_NEWS(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    return news_services.News_Services.GET_TN_NEWS()


@router.post('/news', status_code=status.HTTP_201_CREATED)
def SAVE_NEW(request: news_schema, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    return news_services.News_Services.SAVE_NEWS(request, db, user_id=current_user["userId"])


@router.get("/news", status_code=status.HTTP_200_OK, response_model=List[response_news_schemna])
def GET_NEWS(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    return news_services.News_Services.GET_NEWS(db, user_id=current_user["userId"], user_role=current_user["userRole"])


@router.delete("/news/{id}", status_code=status.HTTP_200_OK)
def DELETE_NEWS(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    return news_services.News_Services.DELETE_NEWS(id, db)


@router.get("/news/{id}", status_code=status.HTTP_200_OK, response_model=response_news_schemna)
def GET_NEWS(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    return news_services.News_Services.GET_SINGLE_NEW(id, db, user_role=current_user["userRole"], user_id=current_user["userId"])
