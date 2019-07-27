from datetime import datetime
from sqlalchemy.orm import relationship

from web_app import db

# Отзывы


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    resolved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = relationship("User", back_populates="reviews")

    def set_resolved(self, resolved: bool):
        self.resolved = resolved
        db.session.commit()
        return self

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
        self.current_menu = current_menu if current_menu is not None else self.current_menu
        self.special_index = special_index if special_index is not None else self.special_index
        db.session.commit()
        return self