from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from config.config import Config

engine = create_engine(Config.DATABASE, echo=False)
Base = declarative_base()

class UserAnswer(Base):
    __tablename__ = 'user_answers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    answer = Column(String)
    user = relationship("User", backref="user_answers")

class UserCache(Base):
    __tablename__ = 'user_cache'
    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, ForeignKey('users.id'))
    current_menu = Column(String)
    special_index = Column(Integer, default=0)
    child = relationship("User", uselist=False, back_populates="user_cache")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    vk_id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    total_requests = Column(Integer, default=0)
    cache_id = Column(Integer, ForeignKey('user_cache.id'))
    cache = relationship("UserCache", back_populates="users")

    created_date = Column(DateTime, index=True, default=datetime.utcnow)
    update_date = Column(DateTime, onupdate=datetime.utcnow)

    def __init__(self, vk_id: int, first_name: str, last_name: str, current_menu: str):
        self.vk_id = vk_id
        self.first_name = first_name
        self.last_name = last_name
        self.current_menu = current_menu

    def __repr__(self):
        return "<User('%s','%s')>" % (self.name, self.currient_menu)


class TypePlace(Base):
    __tablename__ = 'type_place'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    type_place_id = Column(Integer, ForeignKey('type_place.id'))
    type_place = relationship("TypePlace", backref="place")

    map_url = Column(String)
    adress = Column(String)





# Создание таблицы
Base.metadata.create_all(engine)

