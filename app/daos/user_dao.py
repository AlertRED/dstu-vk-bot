from sqlalchemy.orm import Session
from app.models.models import User, UserAnswer, UserCache


class userDAO:

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, vk_id, first_name, last_name, menu_name):
        user = User.create(vk_id, first_name, last_name).create_cache(menu_name)
        return user

    def user_inc_request(self, vk_id):
        user = User.get_user(vk_id).inc_request()
        return user

    def add_answer(self, vk_id, answer):
        user = User.get_user(vk_id).add_answer(answer)
        return user

    def clear_answers(self, vk_id):
        user = User.get_user(vk_id).clear_answers()
        return user

    def update_user(self, vk_id, **kwargs):
        user = User.get_user(vk_id).update(**kwargs)
        return user
