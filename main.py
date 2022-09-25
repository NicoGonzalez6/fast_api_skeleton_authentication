from fastapi import FastAPI
from config import db
from models import models
from routers import user, authentication, games, news
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=db.engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(games.router)
app.include_router(news.router)
