from enum import unique
from pickle import TRUE
from config.db import Base
from sqlalchemy import Column,  Integer, String
from sqlalchemy import UniqueConstraint


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email"),)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30))
    email = Column(String(100))
    password = Column(String(200))
