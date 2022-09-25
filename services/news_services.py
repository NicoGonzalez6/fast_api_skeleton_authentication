
import requests
import bs4
from sqlalchemy.orm import Session
from schemas.news import news_schema
from models import models
from fastapi import status, HTTPException


class News_Services():

    def Get_DC_NEWS():
        base_url = "https://www.diariodecuyo.com.ar/seccion/san-juan/"
        res = requests.get(base_url)
        soup = bs4.BeautifulSoup(res.text, "lxml")

        news = soup.select(".entry-builder")

        all_news = []
        all_news_filter = []

        for new in news:
            all_news.append({"titles": new.select("h1 a"),
                            "subtitle": new.find_all("p"),
                             "image": new.select("figure a img"),
                             "link": new.select("h1 a")})

        for new in all_news:

            if len(new["subtitle"]) == 0 or len(new["image"]) == 0:
                continue
            else:

                all_news_filter.append(
                    {"title": new["titles"][0].text, "subtitle": new["subtitle"][0].text, "image": "https://www.diariodecuyo.com.ar"+new["image"][0]["src"], "link": "https://www.diariodecuyo.com.ar"+new["link"][0]["href"]})

        return all_news_filter

    def GET_TN_NEWS():
        base_url = "https://tn.com.ar/"
        res = requests.get(base_url)
        soup = bs4.BeautifulSoup(res.text, "lxml")

        news = soup.select(".card__container")

        all_news = []
        all_news_filter = []

        for new in news:
            all_news.append({"titles": new.select(
                ".card__headline a"),  "images": new.select(".responsive-image img"), "link": new.select(".card__image")})

        for new in all_news:

            if len(new["link"]) == 0:
                continue
            else:
                all_news_filter.append(
                    {"title": new["titles"][0].text, "subtitle": "", "image": new["images"][0]["src"], "link": "https://tn.com.ar"+new["link"][0]["href"]})
        return all_news_filter

    def SAVE_NEWS(request: news_schema, db: Session, user_id: int):
        new_news = models.News(title=request.title, subtitle=request.subtitle,
                               link=request.link, image=request.image, page=request.page, user_id=user_id)
        db.add(new_news)
        db.commit()
        db.refresh(new_news)
        return new_news

    def GET_NEWS(db: Session, user_id: int, user_role: str):
        if user_role == "ADMIN":
            news = db.query(models.News).all()
            return news
        else:
            news = db.query(models.News).filter(
                models.News.user_id == user_id).all()
            return news

    def DELETE_NEWS(id: int, db: Session):
        news = db.query(models.News).filter(models.News.id).first()
        db.delete(news)
        db.commit()
        return {"details": True}

    def GET_SINGLE_NEW(id: int, db: Session,  user_role: str, user_id: int):
        if user_role == "ADMIN":
            news = db.query(models.News).filter(models.News.id == id).first()
            return news
        else:
            news = db.query(models.News).filter(
                models.News.id == id).filter_by(user_id=user_id).first()
            if not news:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"No news found with id {id}")
            return news
