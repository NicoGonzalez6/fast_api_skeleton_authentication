from config.db import Base
from sqlalchemy import Column,  Integer, String, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from enum import Enum


class Roles(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email"),)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30))
    email = Column(String(100))
    password = Column(String(200))
    role = Column(String(200), default=Roles.USER)
    news = relationship("Games_News", back_populates="creator")
    news_real = relationship("News", back_populates="creator")


class Games_News(Base):
    __tablename__ = "games_news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(700))
    span = Column(String(700))
    subtitle = Column(String(700))
    link = Column(String(700))
    image = Column(String(700))
    comments = Column(String(700))
    page = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User",  back_populates="news")


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    subtitle = Column(String(400), nullable=True)
    image = Column(String(200))
    link = Column(String(400))
    page = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User",  back_populates="news_real")
