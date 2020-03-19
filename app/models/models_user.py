from app.models.models_DB import *


# Отзывы
class Review(Base):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    resolved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = relationship("User", back_populates="reviews")

    def set_resolved(self, resolved: bool):
        self.resolved = resolved
        session.commit()
        return self

    def __repr__(self):
        return self.message


# User
class UserAnswer(Base):
    __tablename__ = 'user_answers'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = relationship("User", back_populates="answers")

    def __repr__(self):
        return self.answer


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    vk_id = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    total_requests = db.Column(db.Integer, default=0)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    group = relationship("Group", back_populates="users")

    dinamic_items = relationship("DinamicItems", uselist=True, back_populates="user")

    remind = db.Column(db.Boolean, default=False, nullable=False)
    remind_date = db.Column(db.DateTime)
    remind_offset = db.Column(db.Integer, default=0, nullable=False)  # change on offset and Time type

    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, onupdate=datetime.utcnow)

    answers = relationship("UserAnswer", uselist=True, back_populates="user")
    user_cache = relationship("UserCache", uselist=False, back_populates="user")
    reviews = relationship("Review", back_populates="user")

    def __repr__(self):
        return '%s %s' % (self.last_name, self.first_name)

    def refresh_nearest_remind(self):
        current_date = datetime.now()
        current_weekday = current_date.weekday()
        current_week = cw()
        for i in range(1 + current_weekday, 14 + current_weekday):
            schedule = self.get_group().get_schedule(day=days_of_week[i % 7],
                                                     week=2 - (((i // 7) % 2 + current_week) % 2))
            if schedule:
                self.remind_date = datetime(current_date.year, current_date.month, current_date.day)
                offset_hours = pairs_time[schedule[0].number].hour - self.remind_offset // 60
                offset_minutes = pairs_time[schedule[0].number].minute - self.remind_offset % 60
                self.remind_date += timedelta(days=i - current_weekday, hours=offset_hours, minutes=offset_minutes)
                session.commit()
        return self

    def get_group(self):
        return self.group

    @staticmethod
    def get_users_remind():
        min_date = session.query(func.min(User.remind_date)).first()
        users = session.query(User).filter_by(remind_date=min_date, remind=True).all()
        return min_date, users

    @change_notify
    def set_remind(self, remind: bool):
        self.remind = remind
        session.commit()
        return self

    def inc_request(self, inc=1):
        self.total_requests += inc
        session.commit()
        return self

    def add_review(self, message):
        self.reviews.append(Review(message=message))
        session.commit()
        return self

    # не используется
    def add_answer(self, answer):
        self.answers.append(UserAnswer(answer=answer))
        session.commit()
        return self

    def set_answers(self, answers: list):
        for answer in self.answers:
            session.delete(answer)
        session.commit()
        for answer in answers:
            self.answers.append(UserAnswer(answer=answer))
        session.commit()
        return self

    def clear_answers(self):
        self.answers = []
        session.commit()
        return self

    def set_index(self, index: int):
        self.user_cache.update(special_index=index)
        return self

    def set_menu(self, menu_name: str):
        self.user_cache.update(current_menu=menu_name)
        return self

    @change_notify
    def __update_group(self, group_name=None):
        self.group = self.group.get_group(group_name)

    def update(self, vk_id=None, first_name=None, last_name=None, total_requests=None, group_name=None):
        self.vk_id = vk_id if vk_id else self.vk_id
        self.first_name = first_name if first_name else self.first_name
        self.last_name = last_name if last_name else self.last_name
        self.total_requests = total_requests if total_requests else self.total_requests
        if group_name and (not self.group or self.group.name != group_name):
            self.__update_group(group_name=group_name)
        session.commit()
        return self

    def create_cache(self, start_menu=None):
        if not self.user_cache:
            self.user_cache = UserCache(current_menu=start_menu)
        return self

    @staticmethod
    def get_user(vk_id):
        return session.query(User).filter_by(vk_id=vk_id).first()

    @staticmethod
    def create(vk_id, first_name, last_name):
        user = User.get_user(vk_id)
        if not user:
            user = User(vk_id, first_name=first_name, last_name=last_name)
            session.add(user)
            session.commit()
        return user

    def __init__(self, vk_id: int, first_name: str, last_name: str):
        self.vk_id = vk_id
        self.first_name = first_name
        self.last_name = last_name

    def add_dinamic_items(self, index_name, dinamic_name):
        DinamicItems.create(index_name=index_name, dinamic_name=dinamic_name)
        return self

    def delete_all_dinamic_items(self):
        self.dinamic_items = []
        session.commit()
        return self

    def get_dinamic_item(self, index_name=None, dinamic_name=None):
        return DinamicItems.get_frist(dinamic_name=dinamic_name)


class DinamicItems(Base):
    __tablename__ = 'dinamic_items'
    id = db.Column(db.Integer, primary_key=True)
    index_name = db.Column(db.String)
    dinamic_name = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="dinamic_items")

    @staticmethod
    def get(index_name, dinamic_name):
        return session.query(DinamicItems).filter_by(index_name=index_name, dinamic_name=dinamic_name).first()

    @staticmethod
    def create(index_name, dinamic_name):
        item = DinamicItems.get(index_name=index_name, dinamic_name=dinamic_name)
        if not item:
            item = DinamicItems(index_name=index_name, dinamic_name=dinamic_name)
            session.add(item)
            session.commit()
        return item

    @staticmethod
    def get_frist(index_name=None, dinamic_name=None):
        return session.query(DinamicItems).filter_by(dinamic_name=dinamic_name).first()




class UserCache(Base):
    __tablename__ = 'user_cache'
    id = db.Column(db.Integer, primary_key=True)
    current_menu = db.Column(db.String)
    special_index = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="user_cache")

    def __repr__(self):
        return '<current_menu: %s>' % self.current_menu

    def update(self, current_menu=None, special_index=None):
        self.current_menu = current_menu if current_menu is not None else self.current_menu
        self.special_index = special_index if special_index is not None else self.special_index
        session.commit()
        return self
