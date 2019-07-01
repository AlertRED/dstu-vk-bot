from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time, Boolean, Enum
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from config.conf import Config

engine = create_engine(Config.DATABASE, echo=False)
Base = declarative_base()


class UserAnswer(Base):
    __tablename__ = 'user_answers'
    id = Column(Integer, primary_key=True)
    answer = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", backref="user_answers")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    vk_id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    total_requests = Column(Integer, default=0)
    created_date = Column(DateTime, index=True, default=datetime.utcnow)
    update_date = Column(DateTime, onupdate=datetime.utcnow)

    answers = relationship("UserAnswer", back_populates="user")
    user_cache = relationship("UserCache", uselist=False, back_populates="user")

    def inc_request(self, inc=1):
        self.total_requests += inc
        engine.commit()
        return self

    def add_answer(self, answer):
        self.answers.append(UserAnswer(answer=answer))
        engine.commit()
        return self

    def clear_answers(self):
        self.answers = []
        engine.commit()
        return self

    def update(self, vk_id=None, first_name=None, last_name=None, total_requests=None, user_cache=None, answers=None):
        self.vk_id = vk_id if vk_id else self.vk_id
        self.first_name = first_name if first_name else self.first_name
        self.last_name = last_name if last_name else self.last_name
        self.total_requests = total_requests if total_requests else self.total_requests
        self.user_cache = user_cache if user_cache else self.user_cache
        self.answers = answers if answers else self.answers
        engine.commit()
        return self

    def create_cache(self, start_menu):
        self.user_cache = UserCache(current_menu=start_menu)
        return self

    @staticmethod
    def get_user(vk_id):
        return engine.query(User).filter_by(vk_id=vk_id).first()

    @staticmethod
    def create(vk_id, first_name, last_name):
        user = User.get_user(vk_id)
        if not user:
            user = User(vk_id, first_name=first_name, last_name=last_name)
            engine.add(user)
            engine.commit()
        return user

    def delete(self, vk_id):
        engine.delete(User.get_user(vk_id))
        engine.commit()

    def __init__(self, vk_id: int, first_name: str, last_name: str):
        self.vk_id = vk_id
        self.first_name = first_name
        self.last_name = last_name


class UserCache(Base):
    __tablename__ = 'user_cache'
    id = Column(Integer, primary_key=True)
    current_menu = Column(String)
    special_index = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="user_cache")

    def update(self, currient_menu=None, special_index=None):
        self.current_menu = currient_menu
        self.special_index = special_index
        engine.commit()
        return self


class TypePlace(Base):
    __tablename__ = 'type_place'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    places = relationship("Place", back_populates="type_place")


class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    map_url = Column(String)
    img_name = Column(String)
    adress = Column(String)

    type_place_id = Column(Integer, ForeignKey('type_place.id'))
    type_place = relationship("TypePlace", back_populates="places")
    faculty = relationship("Faculty", back_populates="place")
    schedules = relationship("Schedule_place", back_populates="place")
    managers = relationship("Manager", back_populates="place")
    phones = relationship("Phone_place", back_populates="place")


class Schedule_place(Base):
    __tablename__ = 'schedule_place'
    id = Column(Integer, primary_key=True)
    start_time = Column(Time)
    end_time = Column(Time)
    pause_start_time = Column(Time)
    pause_end_time = Column(Time)

    place_id = Column(Integer, ForeignKey('place.id'))
    place = relationship("Place", back_populates="schedules")
    day_of_week_id = Column(Integer, ForeignKey('day_of_week.id'))
    day_of_week = relationship("Day_of_week", back_populates="schedules")


class Day_of_week(Base):
    __tablename__ = 'day_of_week'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    schedules = relationship("Schedule_place", back_populates="day_of_week")


class Manager(Base):
    __tablename__ = 'managers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)

    place_id = Column(Integer, ForeignKey('place.id'))
    place = relationship("Place", back_populates="managers")

    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("Post", back_populates="managers")


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    managers = relationship("Manager", back_populates="post")


class Phone_place(Base):
    __tablename__ = 'phone_place'
    id = Column(Integer, primary_key=True)
    phone = Column(String)

    place_id = Column(Integer, ForeignKey('place.id'))
    place = relationship("Place", back_populates="phones")


class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    abbreviation = Column(String, nullable=False)
    cabinet_dean = Column(String, nullable=False)
    cabinet_dean_office = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    place_id = Column(Integer, ForeignKey('place.id'))
    place = relationship('Place', uselist=False, back_populates="faculty")

    schedules = relationship("Schedule_dean_office", back_populates="faculty")
    dean = relationship("Dean", uselist=False, back_populates="faculty")
    departments = relationship("Department", back_populates="faculty")
    specialties = relationship("Specialty", back_populates="faculty")


class Schedule_dean_office(Base):
    __tablename__ = 'schedule_dean_office'
    id = Column(Integer, primary_key=True)
    start_time = Column(Time)
    end_time = Column(Time)
    pause_start_time = Column(Time)
    pause_end_time = Column(Time)

    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="schedules")
    day_of_week_id = Column(Integer, ForeignKey('day_of_week.id'))
    day_of_week = relationship("Day_of_week", back_populates="schedules")


class Dean(Base):
    __tablename__ = 'dean'
    id = Column(Integer, primary_key=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)

    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="dean")


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    abbreviation = Column(String, nullable=False)
    cabinet = Column(String, nullable=False)
    description = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="departments")

    manager = relationship("Manager_department", uselist=False, back_populates="department")


class Manager_department(Base):
    __tablename__ = 'manager_department'
    id = Column(Integer, primary_key=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)

    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship("Department", back_populates="manager")


class Specialty(Base):
    __tablename__ = 'specialty'
    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    abbreviation = Column(String, nullable=False)

    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="specialties")
    types = relationship("Type_specialty", back_populates="specialty")


class Type_specialty(Base):
    __tablename__ = 'type_specialty'
    id = Column(Integer, primary_key=True)

    code = Column(String, nullable=False)
    type = Column(Enum('Бакалавриат', 'Магистратура', 'Аспирантура', name="type_specialty_enum"), nullable=False)
    duration = Column(Integer, nullable=False)

    specialty_id = Column(Integer, ForeignKey('specialty.id'))
    specialty = relationship("Specialty", back_populates="types")


# Создание таблицы
Base.metadata.create_all(engine)
