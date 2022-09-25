
import requests
import bs4
from schemas.game_news_schema import Game_News_Schema
from sqlalchemy.orm import Session
from models import models
from fastapi import status, HTTPException


class Games_Services():

    def get_games_news(page: int):

        base_url = "https://www.3djuegos.com/novedades/todo/juegos/{}pf0f0f0/fecha/"

        scrape_url = base_url.format(page)
        res = requests.get(scrape_url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        news = soup.select(".nov_int")

        titles = []
        title_list = []

        for new in news:
            titles.append({"title": new.select(".wi100 h2"),
                          "span": new.select(".col_plat"), "subtitle": new.select(".dn600"), "link": new.select(".wi100 h2 a"), "image": new.select(".pr figure a img"), "comments": new.select(".nov_main_fec a")})
        for title in titles:

            if len(title["image"]) == 0 or len(title["comments"]) == 0:
                continue
            else:
                title_list.append(
                    {"title": title["title"][0].select("h2 a")[0]["title"], "span": title["span"][0].text, "subtitle": title["subtitle"][0].text, "link": title["link"][0]["href"], "image": title["image"][0]["data-src"], "comments": title["comments"][0].text})

        return title_list

    def get_spot_news(page: int):
        base_url = "https://www.gamespot.com/news/?page={}"

        scrape_url = base_url.format(page)

        res = requests.get(scrape_url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        news = soup.select(".card-item")

        titles = []
        title_list = []
        for new in news:
            titles.append({"span": new.select(".card-item__label"),
                          "title": new.select(".card-item__content a h4"),
                           "image": new.select(".card-item__img img"),
                           "comments": new.select(".symbol-text span")[0],
                           "link": new.select(".card-item__content a")
                           })

        for title in titles:
            print()
            title_list.append(
                {"title": title["title"][0].text, "image": title["image"][0]["src"], "comments": title["comments"].text, "span": title["span"][0].text, "subtitle": None, "link": "https://www.gamespot.com"+title["link"][0]["href"]})

        return title_list

    def save_game_new(request: Game_News_Schema, db: Session, user_id: int):
        news = models.Games_News(
            title=request.title, span=request.span, subtitle=request.subtitle, link=request.link, image=request.image, comments=request.comments, page=request.page, user_id=user_id)
        db.add(news)
        db.commit()
        db.refresh(news)
        return news

    def delete_game_new(id: int, db: Session):
        new = db.query(models.Games_News).filter(
            models.Games_News.id == id).first()
        if not new:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"no news with id {id}")
        db.delete(new)
        db.commit()
        return {"details": True}

    def saved_news(db: Session, user_role: str, user_id: int):
        if user_role == "ADMIN":
            all_news = db.query(models.Games_News).all()
            return all_news
        else:
            all_news = db.query(models.Games_News).filter(
                models.Games_News.user_id == user_id).all()
            return all_news

    def get_single_game_new(id: int, db: Session,  user_role: str, user_id: int):
        if user_role == "ADMIN":
            news = db.query(models.Games_News).filter(
                models.Games_News.id == id).first()
            return news
        else:
            news = db.query(models.Games_News).filter(
                models.Games_News.id == id).filter_by(user_id=user_id).first()
            if not news:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"No news found with id {id}")
            return news
