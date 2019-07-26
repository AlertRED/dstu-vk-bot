from app.models.models import *

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
    departments = relationship("Department", back_populates="place")
    schedules = relationship("SchedulePlace", back_populates="place")
    managers = relationship("ManagerPlace", back_populates="place")
    phones = db.Column(ARRAY(db.String), server_default="{}")

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
        self.managers.append(ManagerDepartment.create(first_name, last_name, patronymic).add_post(post_name))
        return self

    def set_phones(self, phones: list):
        self.phones.clear()
        for phone in phones:
            self.phones.append(phone)
        db.session.commit()
        return self

    # def set_phones(self, phones: list):
    #     for phone in self.phones:
    #         db.session.delete(phone)
    #     db.session.commit()
    #     for phone in phones:
    #         self.phones.append(PhonePlace(phone=phone))
    #     db.session.commit()
    #     return self

    def add_type_place(self, type_name):
        self.type_place = TypePlace.create(type_name)
        db.session.commit()
        return self

    def add_schedule(self, day_name, start_time, end_time, pause_start_time=None, pause_end_time=None):
        schedule = SchedulePlace.get_schedule(self, day_name)
        if not schedule:
            self.schedules.append(
                SchedulePlace.create(start_time, end_time, pause_start_time, pause_end_time).add_day_of_week(day_name))
        db.session.commit()
        return self


class SchedulePlace(db.Model):
    __tablename__ = 'schedule_place'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    pause_start_time = db.Column(db.Time)
    pause_end_time = db.Column(db.Time)
    day_of_week = db.Column(days_of_week_enum)

    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    place = relationship("Place", back_populates="schedules")

    def __repr__(self):
        return '%s. %s - %s (%s - %s)' % (
            self.day_of_week, self.start_time, self.end_time, self.pause_start_time, self.pause_end_time)

    def add_day_of_week(self, name):
        self.day_of_week = name
        db.session.commit()
        return self


    @staticmethod
    def get_schedule(place, day_name):
        return db.session.query(SchedulePlace).filter_by(place=place,
                                                         day_of_week=day_name).first()

    @staticmethod
    def create(start_time, end_time, pause_start_time, pause_end_time):
        schedule = SchedulePlace(start_time=start_time, end_time=end_time, pause_start_time=pause_start_time,
                                 pause_end_time=pause_end_time)
        db.session.add(schedule)
        db.session.commit()
        return schedule



class ManagerPlace(db.Model):
    __tablename__ = 'manager_place'
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
        return db.session.query(ManagerDepartment).filter_by(first_name=first_name, last_name=last_name,
                                                             patronymic=patronymic).first()

    @staticmethod
    def create(first_name, last_name, patronymic):
        manager = ManagerPlace.get_manager(first_name, last_name, patronymic)
        if not manager:
            manager = ManagerDepartment(first_name=first_name, last_name=last_name, patronymic=patronymic)
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
    managers = relationship("ManagerPlace", back_populates="post")

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


# class PhonePlace(db.Model):
#     __tablename__ = 'phone_place'
#     id = db.Column(db.Integer, primary_key=True)
#     phone = db.Column(db.String)
#
#     def __repr__(self):
#         return self.phone
#
#     place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
#     place = relationship("Place", back_populates="phones")