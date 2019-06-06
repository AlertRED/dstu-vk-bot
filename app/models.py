from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from config.config import Config

engine = create_engine(Config.DATABASE, echo=False)
Base = declarative_base()

class UserAnswer(Base):
    __tablename__ = 'user_answers'
    id = Column(Integer, primary_key=True)
    answer = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="user_answers")

class UserCache(Base):
    __tablename__ = 'user_cache'
    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, ForeignKey('users.id'))
    current_menu = Column(String)
    special_index = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", uselist=False, back_populates="user_cache")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    vk_id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    total_requests = Column(Integer, default=0)
    created_date = Column(DateTime, index=True, default=datetime.utcnow)
    update_date = Column(DateTime, onupdate=datetime.utcnow)

    answers = relationship("UserAnswer", back_populates="users")
    cache = relationship("UserCache", back_populates="users")



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
    places = relationship("Place", back_populates="type_place")

class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    map_url = Column(String)
    adress = Column(String)

    type_place_id = Column(Integer, ForeignKey('type_place.id'))
    type_place = relationship("TypePlace", backref="place")
    schedules = relationship("Schedule", backref="place")
    managers = relationship("Manager", backref="")

class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    start_time = Column(Time)
    end_time = Column(Time)
    pause_start_time = Column(Time)
    pause_end_time = Column(Time)

    place_id = Column(Integer, nullable=False)
    place = relationship("Place", backref="schedule")

    day_of_week_id = Column(Integer, nullable=False)
    day_of_week = relationship("Day_of_week", backref="schedule")


class Day_of_week(Base):
    __tablename__ = 'day_of_week'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    schedules = relationship("Schedule", backref="day_of_week")



class Manager(Base):
    __tablename__ = 'managers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)

    place_id = Column(Integer, nullable=False)
    place = relationship("Place", backref="managers")
    post_id = Column(Integer, nullable=False)
    posts = relationship("Post", backref="managers")


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    managers = relationship("Manager", backref="posts")



# Создание таблицы
Base.metadata.create_all(engine)

