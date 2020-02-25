from app.models_menu import Menu
from app.models.orm_models import User


class Controller:

    @staticmethod
    def __parse_answer(data_answer: dict, user: User, current_menu: Menu):
        answer = data_answer.get("answer", None)
        current_menu = data_answer.get("new_menu", current_menu)
        special_answers = data_answer.get("special_answers", [])
        special_index = data_answer.get("special_index", None)

        user.set_index(special_index).set_menu(current_menu.index).set_answers(special_answers)
        return answer, current_menu

    def get_answer(self, request: str, user: User):
        current_menu = Menu.menues[int(user.user_cache.current_menu)]
        result = current_menu.get_answer(request,
                                         special_index=user.user_cache.special_index,
                                         special_answers=[i.answer for i in user.answers],
                                         vk_id=user.vk_id)

        result = self.__parse_answer(result, user, current_menu)
        return result
