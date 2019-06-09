from sqlalchemy import Time
from sqlalchemy.orm import Session
from app.models import User, UserAnswer, UserCache


class userDAO:

    def __init__(self, db: Session):
        self.db = db

    def first_or_create_user(self, vk_id, first_name, last_name, menu_name):
        user = self.db.query(User).filter_by(vk_id=vk_id).first()
        if not user:
            user_cache = UserCache(current_menu=menu_name)
            user = User(vk_id, first_name=first_name, last_name=last_name)
            user.user_cache = user_cache

            self.db.add(user)
            self.db.commit()
        return user

    def user_inc_request(self, vk_id, inc=1):
        user = self.db.query(User).filter_by(vk_id=vk_id).first()
        user.total_requests += inc
        self.db.commit()
        return user

    def update_user(self, vk_id, **kwargs):
        user = self.db.query(User).filter_by(vk_id=vk_id).first()
        if kwargs.get("first_name") is not None:
            user.first_name = kwargs.get("first_name", user.first_name)
        if kwargs.get("last_name") is not None:
            user.last_name = kwargs.get("last_name", user.last_name)
        if kwargs.get("total_requests") is not None:
            user.total_requests = kwargs.get("total_requests", user.total_requests)
        if kwargs.get("current_menu") is not None:
            user.user_cache.current_menu = kwargs.get("current_menu", user.user_cache.current_menu)
        if kwargs.get("special_index") is not None:
            user.user_cache.special_index = kwargs.get("special_index", user.user_cache.special_index)
        if kwargs.get("special_answers") is not None:
            user.answers = [UserAnswer(answer=answer) for answer in kwargs.get("special_answers", [])]

        self.db.commit()
        return user
