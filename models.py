from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref

engine = create_engine('postgresql://postgres@127.0.0.1/mydb', echo=False)
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
    vk_id = Column(Integer)
    name = Column(String)
    current_menu = Column(String)
    special_index = Column(Integer, default=0)


    def __init__(self, name, vk_id, current_menu):
        self.name = name
        self.vk_id = vk_id
        self.current_menu = current_menu

    def __repr__(self):
        return "<User('%s','%s')>" % (self.name, self.currient_menu)


# Создание таблицы
Base.metadata.create_all(engine)