from sqlalchemy.orm import Session
from menues import root
from models import User, Answer


class userDAO:

    def __init__(self, db: Session):
        self.db = db

    def first_or_create_user(self, vk_id):
        user = self.db.query(User).filter_by(vk_id=vk_id).first()
        if not user:
            user = User("username", vk_id, root.name)
            self.db.add(user)
            self.db.commit()
        return user

    def update_user(self, vk_id, **kwargs):
        user = self.db.query(User).filter_by(vk_id=vk_id).first()

        if kwargs.get("current_menu", None) != None:
            user.current_menu = kwargs.get("current_menu", user.current_menu)

        if kwargs.get("name", None):
            user.name = kwargs.get("name", user.name)

        if kwargs.get("special_index", None) != None:
            user.special_index = kwargs.get("special_index", user.special_index)

        if kwargs.get("special_answers", None) != None:
            answers = []
            for answer in kwargs.get("special_answers"):
                answers.append(Answer(answer=answer))
            user.answers = answers

        self.db.commit()
        return user