from fastapi import FastAPI
from config import db
from models import models
from routers import user, authentication

app = FastAPI()

models.Base.metadata.create_all(bind=db.engine)

app.include_router(authentication.router)
app.include_router(user.router)
