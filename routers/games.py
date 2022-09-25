from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.db import get_db
from utils import oauth2
from services import games_services
from schemas.game_news_schema import Game_News_Schema, Show_Games_schema


router = APIRouter(
    prefix="/Games",
    tags=["Games"]
)


@router.get('/3dgames/{page}', status_code=status.HTTP_200_OK)
def GET_3D_GAMES_NEWS(page: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    return games_services.Games_Services.get_games_news(page)


@router.get('/game_spot/{page}', status_code=status.HTTP_200_OK)
def GET_GAMES_SPOT_NEWS(page: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    return games_services.Games_Services.get_spot_news(page)


@router.post('/game_news', status_code=status.HTTP_201_CREATED)
def SAVE_GAME_NEWS(request: Game_News_Schema, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    return games_services.Games_Services.save_game_new(request, db, user_id=current_user["userId"])


@router.delete('/game_news/{id}',  status_code=status.HTTP_200_OK)
def DELETE_GAME_NEWS(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    return games_services.Games_Services.delete_game_new(id, db)


@router.get('/game_news',  status_code=status.HTTP_200_OK, response_model=List[Show_Games_schema])
def GET_SAVED_NEWS(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    return games_services.Games_Services.saved_news(db, user_role=current_user["userRole"], user_id=current_user["userId"])


@router.get("/game_news/{id}", status_code=status.HTTP_200_OK, response_model=Show_Games_schema)
def GET_NEWS(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    return games_services.Games_Services.get_single_game_new(id, db, user_role=current_user["userRole"], user_id=current_user["userId"])
