from datetime import datetime
from sqlalchemy.orm import relationship
import web_app.__init__ as flask

db = flask.db

days_of_week = ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс')
days_of_week_enum = db.Enum(*days_of_week, name="days_of_week")

# Отзывы
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = relationship("User", back_populates="reviews")

    def __repr__(self):
        return self.message

# User
class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = relationship("User", back_populates="answers")

    def __repr__(self):
        return self.answer


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    vk_id = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    total_requests = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, onupdate=datetime.utcnow)

    answers = relationship("UserAnswer", back_populates="user")
    user_cache = relationship("UserCache", uselist=False, back_populates="user")
    reviews = relationship("Review", back_populates="user")

    def __repr__(self):
        return '%s %s' % (self.last_name, self.first_name)

    def inc_request(self, inc=1):
        self.total_requests += inc
        db.session.commit()
        return self

    def add_review(self, message):
        self.reviews.append(Review(message=message))
        db.session.commit()
        return self

    # не используется
    def add_answer(self, answer):
        self.answers.append(UserAnswer(answer=answer))
        db.session.commit()
        return self

    def set_answers(self, answers: list):
        for answer in self.answers:
            db.session.delete(answer)
        db.session.commit()
        for answer in answers:
            self.answers.append(UserAnswer(answer=answer))
        db.session.commit()
        return self

    def clear_answers(self):
        self.answers = []
        db.session.commit()
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
        db.session.commit()
        return self

    def create_cache(self, start_menu=None):
        if not self.user_cache:
            self.user_cache = UserCache(current_menu=start_menu)
        return self

    @staticmethod
    def get_user(vk_id):
        return db.session.query(User).filter_by(vk_id=vk_id).first()

    @staticmethod
    def create(vk_id, first_name, last_name):
        user = User.get_user(vk_id)
        if not user:
            user = User(vk_id, first_name=first_name, last_name=last_name)
            db.session.add(user)
            db.session.commit()
        return user

    def __init__(self, vk_id: int, first_name: str, last_name: str):
        self.vk_id = vk_id
        self.first_name = first_name
        self.last_name = last_name


class UserCache(db.Model):
    __tablename__ = 'user_cache'
    id = db.Column(db.Integer, primary_key=True)
    current_menu = db.Column(db.String)
    special_index = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="user_cache")

    def __repr__(self):
        return '<current_menu: %s>' % self.current_menu

    def update(self, current_menu=None, special_index=None):
        self.current_menu = current_menu if current_menu else self.current_menu
        self.special_index = special_index if special_index is not None else self.special_index
        db.session.commit()
        return self


# Place ##########################################################################################

class TypePlace(db.Model):
    __tablename__ = 'type_place'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    places = relationship("Place", back_populates="type_place")

    @staticmethod
    def get_type_place(name):
        return db.session.query(TypePlace).filter_by(name=name).first()

    @staticmethod
    def create(name):
        type_place = TypePlace.get_type_place(name)
        if not type_place:
            type_place = TypePlace(name=name)
        return type_place

    def __repr__(self):
        return self.name


class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    map_url = db.Column(db.String)
    img_name = db.Column(db.String)
    adress = db.Column(db.String)

    type_place_id = db.Column(db.Integer, db.ForeignKey('type_place.id'))
    type_place = relationship("TypePlace", back_populates="places")
    faculties = relationship("Faculty", back_populates="place")
    schedules = relationship("Schedule_place", back_populates="place")
    managers = relationship("Manager", back_populates="place")
    phones = relationship("Phone_place", back_populates="place")

    def __repr__(self):
        return self.name

    @staticmethod
    def get_places_by_type(type_name):
        type_place = TypePlace.get_type_place(type_name)
        places = db.session.query(Place).filter_by(type_place=type_place).all()
        return places

    @staticmethod
    def get_place(name):
        return db.session.query(Place).filter_by(name=name).first()

    @staticmethod
    def create(name, map_url, img_name, adress):
        place = Place.get_place(name)
        if not place:
            place = Place(name=name, map_url=map_url, img_name=img_name, adress=adress)
            db.session.add(place)
            db.session.commit()
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
        db.session.commit()
        return self

    def add_manager(self, first_name, last_name, patronymic, post_name):
        self.managers.append(Manager.create(first_name, last_name, patronymic).add_post(post_name))
        return self

    def set_phones(self, phones: list):
        for phone in self.phones:
            db.session.delete(phone)
        db.session.commit()
        for phone in phones:
            self.phones.append(Phone_place(phone=phone))
        db.session.commit()
        return self

    def add_type_place(self, type_name):
        self.type_place = TypePlace.create(type_name)
        db.session.commit()
        return self

    def add_schedule(self, day_name, start_time, end_time, pause_start_time=None, pause_end_time=None):
        schedule = Schedule_place.get_schedule(self, day_name)
        if not schedule:
            self.schedules.append(
                Schedule_place.create(start_time, end_time, pause_start_time, pause_end_time).add_day_of_week(day_name))
        db.session.commit()
        return self


class Schedule_place(db.Model):
    __tablename__ = 'schedule_place'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    pause_start_time = db.Column(db.Time)
    pause_end_time = db.Column(db.Time)

    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    place = relationship("Place", back_populates="schedules")
    day_of_week = db.Column(days_of_week_enum)

    def __repr__(self):
        return '%s. %s - %s (%s - %s)' % (
        self.day_of_week, self.start_time, self.end_time, self.pause_start_time, self.pause_end_time)

    @staticmethod
    def get_schedule(place, day_name):
        return db.session.query(Schedule_place).filter_by(place=place,
                                                          day_of_week=day_name).first()

    @staticmethod
    def create(start_time, end_time, pause_start_time, pause_end_time):
        schedule = Schedule_place(start_time=start_time, end_time=end_time, pause_start_time=pause_start_time,
                                  pause_end_time=pause_end_time)
        db.session.add(schedule)
        db.session.commit()
        return schedule

    def add_day_of_week(self, name):
        self.day_of_week = name
        db.session.commit()
        return self


class Manager(db.Model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    patronymic = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.patronymic)

    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    place = relationship("Place", back_populates="managers")

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = relationship("Post", back_populates="managers")

    @staticmethod
    def get_manager(first_name, last_name, patronymic):
        return db.session.query(Manager).filter_by(first_name=first_name, last_name=last_name,
                                                   patronymic=patronymic).first()

    @staticmethod
    def create(first_name, last_name, patronymic):
        manager = Manager.get_manager(first_name, last_name, patronymic)
        if not manager:
            manager = Manager(first_name=first_name, last_name=last_name, patronymic=patronymic)
            db.session.add(manager)
            db.session.commit()
        return manager

    def add_post(self, post_name):
        self.post = Post.create(post_name)
        return self


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    managers = relationship("Manager", back_populates="post")

    def __repr__(self):
        return self.name

    @staticmethod
    def get_post(name):
        return db.session.query(Post).filter_by(name=name).first()

    @staticmethod
    def create(name):
        post = Post.get_post(name)
        if not post:
            post = Post(name=name)
            db.session.add(post)
            db.session.commit()
        return post


class Phone_place(db.Model):
    __tablename__ = 'phone_place'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String)

    def __repr__(self):
        return self.phone

    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    place = relationship("Place", back_populates="phones")


# Faculty ##########################################################################################

class Specialty(db.Model):
    __tablename__ = 'specialty'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    abbreviation = db.Column(db.String, nullable=False)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="specialties")
    types = relationship("Type_specialty", back_populates="specialty")

    def __repr__(self):
        return self.name

    @staticmethod
    def get_specialty(name):
        return db.session.query(Specialty).filter_by(name=name).first()

    @staticmethod
    def create(name, abbreviation):
        specialty = Specialty.get_specialty(name)
        if not specialty:
            specialty = Specialty(name=name, abbreviation=abbreviation)
            db.session.add(specialty)
            db.session.commit()
        return specialty

    def add_type(self, code, type, duration):
        type_specialty = Type_specialty.get_type_specialty(code)
        if not type_specialty:
            self.types.append(Type_specialty.create(code, type, duration))
        return self


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    abbreviation = db.Column(db.String, nullable=False)
    cabinet = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="departments")

    manager = relationship("Manager_department", uselist=False, back_populates="department")

    def __repr__(self):
        return self.name

    @staticmethod
    def get_department(name):
        return db.session.query(Department).filter_by(name=name).first()

    @staticmethod
    def create(name, abbreviation=None, cabinet=None, description=None, phone=None):
        department = Department.get_department(name)
        if not department:
            department = Department(name=name, abbreviation=abbreviation, cabinet=cabinet, description=description,
                                    phone=phone)
            db.session.add(department)
            db.session.commit()
        return department

    def add_manager(self, first_name, last_name, patronymic):
        self.manager = Manager.create(first_name, last_name, patronymic)
        db.session.commit()
        return self


class Schedule_dean_office(db.Model):
    __tablename__ = 'schedule_dean_office'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    pause_start_time = db.Column(db.Time)
    pause_end_time = db.Column(db.Time)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="schedules")
    day_of_week = db.Column(days_of_week_enum)

    @staticmethod
    def get_schedule(faculty, day_name):
        return db.session.query(Schedule_dean_office).filter_by(faculty=faculty,
                                                                day_of_week=day_name).first()

    def __repr__(self):
        return '%s. %s - %s (%s - %s)' % (
        self.day_of_week, self.start_time, self.end_time, self.pause_start_time, self.pause_end_time)

    @staticmethod
    def create(start_time, end_time, pause_start_time, pause_end_time):
        schedule = Schedule_dean_office(start_time=start_time, end_time=end_time, pause_start_time=pause_start_time,
                                        pause_end_time=pause_end_time)
        db.session.add(schedule)
        db.session.commit()
        return schedule

    def add_day_of_week(self, name):
        self.day_of_week = name
        db.session.commit()
        return self


class Faculty(db.Model):
    __tablename__ = 'faculty'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    abbreviation = db.Column(db.String)
    cabinet_dean = db.Column(db.String)
    cabinet_dean_office = db.Column(db.String)
    phone = db.Column(db.String)

    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    place = relationship('Place', back_populates="faculties")

    schedules = relationship("Schedule_dean_office", back_populates="faculty")
    dean = relationship("Dean", uselist=False, back_populates="faculty")
    departments = relationship("Department", back_populates="faculty")
    specialties = relationship("Specialty", back_populates="faculty")

    def __repr__(self):
        return self.name

    @staticmethod
    def all():
        return db.session.query(Faculty).all()

    @staticmethod
    def get_faculty(name=None, abbreviation=None):
        if name:
            return db.session.query(Faculty).filter_by(name=name).first()
        elif abbreviation:
            return db.session.query(Faculty).filter_by(abbreviation=abbreviation).first()

    @staticmethod
    def create(name, abbreviation, cabinet_dean, cabinet_dean_office, phone):
        faculty = Faculty.get_faculty(name)
        if not faculty:
            faculty = Faculty(name=name, abbreviation=abbreviation, cabinet_dean=cabinet_dean,
                              cabinet_dean_office=cabinet_dean_office, phone=phone)
            db.session.add(faculty)
            db.session.commit()
        return faculty

    def add_dean(self, last_name, first_name, patronymic):
        self.dean = Dean.create(first_name, last_name, patronymic)
        db.session.commit()
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


class Dean(db.Model):
    __tablename__ = 'dean'
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    patronymic = db.Column(db.String, nullable=False)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="dean")

    def __repr__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.patronymic)

    @staticmethod
    def get_dean(first_name, last_name, patronymic):
        return db.session.query(Dean).filter_by(first_name=first_name, last_name=last_name,
                                                patronymic=patronymic).first()

    @staticmethod
    def create(first_name, last_name, patronymic):
        dean = Dean.get_dean(first_name, last_name, patronymic)
        if not dean:
            dean = Dean(first_name=first_name, last_name=last_name, patronymic=patronymic)
            db.session.add(dean)
            db.session.commit()
        return dean


class Manager_department(db.Model):
    __tablename__ = 'manager_department'
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    patronymic = db.Column(db.String, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = relationship("Department", back_populates="manager")

    def __repr__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.patronymic)

    @staticmethod
    def get_dean(first_name, last_name, patronymic):
        return db.session.query(Manager_department).filter_by(first_name=first_name, last_name=last_name,
                                                              patronymic=patronymic).first()

    @staticmethod
    def create(first_name, last_name, patronymic):
        manager = Manager_department.get_dean(first_name, last_name, patronymic)
        if not manager:
            manager = Dean(first_name=first_name, last_name=last_name, patronymic=patronymic)
            db.session.add(manager)
            db.session.commit()
        return manager


class Type_specialty(db.Model):
    __tablename__ = 'type_specialty'
    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String, nullable=False)
    type = db.Column(db.Enum('Бакалавриат', 'Магистратура', 'Аспирантура', name="type_specialty_enum"), nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    specialty_id = db.Column(db.Integer, db.ForeignKey('specialty.id'))
    specialty = relationship("Specialty", back_populates="types")

    def __repr__(self):
        return self.code

    @staticmethod
    def get_type_specialty(code):
        return db.session.query(Type_specialty).filter_by(code=code).first()

    @staticmethod
    def create(code, type, duration):
        type_specialty = Type_specialty.get_type_specialty(code)
        if not type_specialty:
            type_specialty = Type_specialty(code=code, type=type, duration=duration)
            db.session.add(type_specialty)
            db.session.commit()
        return type_specialty


# Создание таблицы
db.Model.metadata.create_all(db.engine)
