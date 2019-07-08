from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time, Boolean, Enum
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from config.conf import Config

engine = create_engine(Config.DATABASE, echo=False)
db = Session(bind=engine)
Base = declarative_base()


# User
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
        db.commit()
        return self

    def add_answer(self, answer):
        self.answers.append(UserAnswer(answer=answer))
        db.commit()
        return self

    def set_answers(self, answers: list):
        self.answers.clear()
        for answer in answers:
            self.answers.append(UserAnswer(answer))
        db.commit()
        return self

    def clear_answers(self):
        self.answers = []
        db.commit()
        return self

    def set_index(self, index: int):
        self.user_cache.update(special_index=index)
        return self

    def set_menu(self, menu_name: str):
        self.user_cache.update(current_menu=menu_name)
        return self

    def update(self, vk_id=None, first_name=None, last_name=None, total_requests=None):
        self.vk_id = vk_id if vk_id else self.vk_id
        self.first_name = first_name if first_name else self.first_name
        self.last_name = last_name if last_name else self.last_name
        self.total_requests = total_requests if total_requests else self.total_requests
        db.commit()
        return self

    def create_cache(self, start_menu=None):
        if not self.user_cache:
            self.user_cache = UserCache(current_menu=start_menu)
        return self

    @staticmethod
    def get_user(vk_id):
        return db.query(User).filter_by(vk_id=vk_id).first()

    @staticmethod
    def create(vk_id, first_name, last_name):
        user = User.get_user(vk_id)
        if not user:
            user = User(vk_id, first_name=first_name, last_name=last_name)
            db.add(user)
            db.commit()
        return user

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

    def update(self, current_menu=None, special_index=None):
        self.current_menu = current_menu if current_menu else self.current_menu
        self.special_index = special_index if special_index else self.special_index
        db.commit()
        return self


# Place

class TypePlace(Base):
    __tablename__ = 'type_place'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    places = relationship("Place", back_populates="type_place")

    @staticmethod
    def get_type_place(name):
        return db.query(TypePlace).filter_by(name=name).first()

    @staticmethod
    def create(name):
        type_place = TypePlace.get_type_place(name)
        if not type_place:
            type_place = TypePlace(name=name)
        return type_place


class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    map_url = Column(String)
    img_name = Column(String)
    adress = Column(String)

    type_place_id = Column(Integer, ForeignKey('type_place.id'))
    type_place = relationship("TypePlace", back_populates="places")
    faculties = relationship("Faculty", back_populates="place")
    schedules = relationship("Schedule_place", back_populates="place")
    managers = relationship("Manager", back_populates="place")
    phones = relationship("Phone_place", back_populates="place")

    @staticmethod
    def get_places_by_type(type_name):
        type_place = TypePlace.get_type_place(type_name)
        places = db.query(Place).filter_by(type_place=type_place).all()
        return places

    @staticmethod
    def get_place(name):
        return db.query(Place).filter_by(name=name).first()

    @staticmethod
    def create(name, map_url, img_name, adress):
        place = Place.get_place(name)
        if not place:
            place = Place(name=name, map_url=map_url, img_name=img_name, adress=adress)
            db.add(place)
            db.commit()
        return place

    def update(self, name=None, map_url=None, img_name=None, adress=None, type_place=None, faculties=None,
               schedules=None,
               managers=None, phones=None):
        self.name = name if name else self.name
        self.map_url = map_url if map_url else self.map_url
        self.img_name = img_name if img_name else self.img_name
        self.adress = adress if adress else self.adress
        self.type_place = type_place if type_place else self.type_place
        self.faculties = faculties if faculties else self.faculties
        self.schedules = schedules if schedules else self.schedules
        self.managers = managers if managers else self.managers
        self.phones = phones if phones else self.phones
        db.commit()
        return self

    def add_manager(self, first_name, last_name, patronymic, post_name):
        self.managers.append(Manager.create(first_name, last_name, patronymic).add_post(post_name))
        return self

    def set_phones(self, phones: list):
        for phone in self.phones:
            db.delete(phone)
        db.commit()
        for phone in phones:
            self.phones.append(Phone_place(phone=phone))
        db.commit()
        return self

    def add_type_place(self, type_name):
        self.type_place = TypePlace.create(type_name)
        db.commit()
        return self

    def add_schedule(self, day_name, start_time, end_time, pause_start_time=None, pause_end_time=None):
        schedule = Schedule_place.get_schedule(self, day_name)
        if not schedule:
            self.schedules.append(
                Schedule_place.create(start_time, end_time, pause_start_time, pause_end_time).add_day_of_week(day_name))
        db.commit()
        return self


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
    day_of_week = relationship("Day_of_week", back_populates="schedules_place")

    @staticmethod
    def get_schedule(place, day_name):
        return db.query(Schedule_place).filter_by(place=place,
                                                  day_of_week=Day_of_week.get_day_of_week(day_name)).first()

    @staticmethod
    def create(start_time, end_time, pause_start_time, pause_end_time):
        schedule = Schedule_place(start_time=start_time, end_time=end_time, pause_start_time=pause_start_time,
                                  pause_end_time=pause_end_time)
        db.add(schedule)
        db.commit()
        return schedule

    def add_day_of_week(self, name):
        self.day_of_week = Day_of_week.create(name)
        db.commit()
        return self


class Day_of_week(Base):
    __tablename__ = 'day_of_week'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    schedules_place = relationship("Schedule_place", back_populates="day_of_week")
    schedules_dean_office = relationship("Schedule_dean_office", back_populates="day_of_week")

    @staticmethod
    def get_day_of_week(name):
        return db.query(Day_of_week).filter_by(name=name).first()

    @staticmethod
    def create(name):
        day_of_week = Day_of_week.get_day_of_week(name)
        if not day_of_week:
            day_of_week = Day_of_week(name=name)
            db.add(day_of_week)
            db.commit()
        return day_of_week


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

    @staticmethod
    def get_manager(first_name, last_name, patronymic):
        return db.query(Manager).filter_by(first_name=first_name, last_name=last_name,
                                           patronymic=patronymic).first()

    @staticmethod
    def create(first_name, last_name, patronymic):
        manager = Manager.get_manager(first_name, last_name, patronymic)
        if not manager:
            manager = Manager(first_name=first_name, last_name=last_name, patronymic=patronymic)
            db.add(manager)
            db.commit()
        return manager

    def add_post(self, post_name):
        self.post = Post.create(post_name)
        return self


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    managers = relationship("Manager", back_populates="post")

    @staticmethod
    def get_post(name):
        return db.query(Post).filter_by(name=name).first()

    @staticmethod
    def create(name):
        post = Post.get_post(name)
        if not post:
            post = Post(name=name)
            db.add(post)
            db.commit()
        return post


class Phone_place(Base):
    __tablename__ = 'phone_place'
    id = Column(Integer, primary_key=True)
    phone = Column(String)

    place_id = Column(Integer, ForeignKey('place.id'))
    place = relationship("Place", back_populates="phones")


# Faculty

class Specialty(Base):
    __tablename__ = 'specialty'
    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    abbreviation = Column(String, nullable=False)

    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="specialties")
    types = relationship("Type_specialty", back_populates="specialty")

    @staticmethod
    def get_specialty(name):
        return db.query(Specialty).filter_by(name=name).first()

    @staticmethod
    def create(name, abbreviation):
        specialty = Specialty.get_specialty(name)
        if not specialty:
            specialty = Specialty(name=name, abbreviation=abbreviation)
            db.add(specialty)
            db.commit()
        return specialty

    def add_type(self, code, type, duration):
        type_specialty = Type_specialty.get_type_specialty(code)
        if not type_specialty:
            self.types.append(Type_specialty.create(code, type, duration))
        return self


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

    @staticmethod
    def get_department(name):
        return db.query(Department).filter_by(name=name).first()

    @staticmethod
    def create(name, abbreviation=None, cabinet=None, description=None, phone=None):
        department = Department.get_department(name)
        if not department:
            department = Department(name=name, abbreviation=abbreviation, cabinet=cabinet, description=description,
                                    phone=phone)
            db.add(department)
            db.commit()
        return department

    def add_manager(self, first_name, last_name, patronymic):
        self.manager = Manager.create(first_name, last_name, patronymic)
        db.commit()
        return self


class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    abbreviation = Column(String)
    cabinet_dean = Column(String)
    cabinet_dean_office = Column(String)
    phone = Column(String)

    place_id = Column(Integer, ForeignKey('place.id'))
    place = relationship('Place', back_populates="faculties")

    schedules = relationship("Schedule_dean_office", back_populates="faculty")
    dean = relationship("Dean", uselist=False, back_populates="faculty")
    departments = relationship("Department", back_populates="faculty")
    specialties = relationship("Specialty", back_populates="faculty")

    @staticmethod
    def get_faculty(name):
        return db.query(Faculty).filter_by(name=name).first()

    @staticmethod
    def create(name, abbreviation, cabinet_dean, cabinet_dean_office, phone):
        faculty = Faculty.get_faculty(name)
        if not faculty:
            faculty = Faculty(name=name, abbreviation=abbreviation, cabinet_dean=cabinet_dean,
                              cabinet_dean_office=cabinet_dean_office, phone=phone)
            db.add(faculty)
            db.commit()
        return faculty

    def add_dean(self, first_name, last_name, patronymic):
        self.dean = Dean.create(first_name, last_name, patronymic)
        db.commit()
        return self

    def add_schedule(self, day_name, start_time, end_time, pause_start_time=None, pause_end_time=None):
        schedule = Schedule_dean_office.get_schedule(self, day_name)
        if not schedule:
            self.schedules.append(
                Schedule_dean_office.create(start_time, end_time, pause_start_time, pause_end_time).add_day_of_week(
                    day_name))
        return self

    def add_departament(self, departament: Department):
        if not departament in self.departments:
            self.departments.append(departament)
        return self

    def add_specialty(self, specialty: Specialty):
        if not specialty in self.specialties:
            self.specialties.append(specialty)
        return self


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
    day_of_week = relationship("Day_of_week", back_populates="schedules_dean_office")

    @staticmethod
    def get_schedule(faculty, day_name):
        return db.query(Schedule_dean_office).filter_by(faculty=faculty,
                                                        day_of_week=Day_of_week.get_day_of_week(day_name)).first()

    @staticmethod
    def create(start_time, end_time, pause_start_time, pause_end_time):
        schedule = Schedule_dean_office(start_time=start_time, end_time=end_time, pause_start_time=pause_start_time,
                                        pause_end_time=pause_end_time)
        db.add(schedule)
        db.commit()
        return schedule

    def add_day_of_week(self, name):
        self.day_of_week = Day_of_week.create(name)
        db.commit()
        return self


class Dean(Base):
    __tablename__ = 'dean'
    id = Column(Integer, primary_key=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)

    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="dean")

    @staticmethod
    def get_dean(first_name, last_name, patronymic):
        return db.query(Dean).filter_by(first_name=first_name, last_name=last_name, patronymic=patronymic).first()

    @staticmethod
    def create(first_name, last_name, patronymic):
        dean = Dean.get_dean(first_name, last_name, patronymic)
        if not dean:
            dean = Dean(first_name=first_name, last_name=last_name, patronymic=patronymic)
            db.add(dean)
            db.commit()
        return dean


class Manager_department(Base):
    __tablename__ = 'manager_department'
    id = Column(Integer, primary_key=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)

    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship("Department", back_populates="manager")

    @staticmethod
    def get_dean(first_name, last_name, patronymic):
        return db.query(Manager_department).filter_by(first_name=first_name, last_name=last_name,
                                                      patronymic=patronymic).first()

    @staticmethod
    def create(first_name, last_name, patronymic):
        manager = Manager_department.get_dean(first_name, last_name, patronymic)
        if not manager:
            manager = Dean(first_name=first_name, last_name=last_name, patronymic=patronymic)
            db.add(manager)
            db.commit()
        return manager


class Type_specialty(Base):
    __tablename__ = 'type_specialty'
    id = Column(Integer, primary_key=True)

    code = Column(String, nullable=False)
    type = Column(Enum('Бакалавриат', 'Магистратура', 'Аспирантура', name="type_specialty_enum"), nullable=False)
    duration = Column(Integer, nullable=False)

    specialty_id = Column(Integer, ForeignKey('specialty.id'))
    specialty = relationship("Specialty", back_populates="types")

    @staticmethod
    def get_type_specialty(code):
        return db.query(Type_specialty).filter_by(code=code).first()

    @staticmethod
    def create(code, type, duration):
        type_specialty = Type_specialty.get_type_specialty(code)
        if not type_specialty:
            type_specialty = Type_specialty(code=code, type=type, duration=duration)
            db.add(type_specialty)
            db.commit()
        return type_specialty


# Создание таблицы
Base.metadata.create_all(engine)
