from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from config import Config

engine = create_engine(Config.DATABASE, echo=False)
Base = declarative_base()


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    answer = Column(String)
    user = relationship("User", backref="answers")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    vk_id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    total_requests = Column(Integer, default=0)
    current_menu = Column(String)
    special_index = Column(Integer, default=0)

    created_date = Column(DateTime, index=True, default=datetime.utcnow)
    update_date = Column(DateTime, onupdate=datetime.utcnow)

    def __init__(self, vk_id: int, first_name: str, last_name: str, current_menu: str):
        self.vk_id = vk_id
        self.first_name = first_name
        self.last_name = last_name
        self.current_menu = current_menu

    def __repr__(self):
        return "<User('%s','%s')>" % (self.name, self.currient_menu)


# Создание таблицы
Base.metadata.create_all(engine)

