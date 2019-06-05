import string
from app.menues import Menu, SpecialMenu
from app.models import User


class Controller:

    def __init__(self, userDAO):
        self.userDAO = userDAO

    def get_clear_question(self, question: str):
        return question.lower().rstrip(string.punctuation)

    def parse_answer(self, result_data: dict, user: User, current_menu: Menu):
        answer = result_data.get("answer", None)
        new_menu = result_data.get("new_menu", None)

        special_answers = None
        special_index = None
        if type(current_menu) is SpecialMenu:
            special_answers = result_data.get("special_answers", None)
            special_index = result_data.get("special_index", None)
        elif type(new_menu) is SpecialMenu:
            special_index = result_data.get("special_index", None)

        if new_menu:
            current_menu = new_menu

        # if type(new_menu) is SpecialMenu:
        #     special_question = answer

        self.userDAO.update_user(user.vk_id, special_answers=special_answers, special_index=special_index,
                                 current_menu=current_menu.name)

        return answer, current_menu

    def get_answer(self, request: str, user):
        current_menu = Menu.menues.get(user.current_menu)
        result = current_menu.get_answer(request, special_index=user.special_index,
                                         special_answers=[i.answer for i in user.answers])

        result = self.parse_answer(result, user, current_menu)
        return result

    def get_menu(self, menu_name):
        currient_menu = Menu.menues.get(menu_name)
        return currient_menu.get_menu()
