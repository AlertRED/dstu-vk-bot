from app.models_menu import Menu
from app.models.models_DB import User


class Controller:

    @staticmethod
    def __parse_answer(data_answer: dict, user: User, current_menu: Menu):
        answer = data_answer.get("answer", None)
        new_menu = data_answer.get("new_menu", None)
        special_answers = data_answer.get("special_answers", [])
        special_index = data_answer.get("special_index", None)

        if new_menu is not None:
            current_menu = new_menu

        user.set_index(special_index).set_menu(current_menu.index).set_answers(special_answers)
        return answer, current_menu


    def get_answer(self, request: str, user: User):
        current_menu = Menu.menus[int(user.user_cache.current_menu)]

        dinamic_item = user.get_dinamic_item(dinamic_name=request)
        if dinamic_item:
            request = dinamic_item.index_name

        result = current_menu.get_answer(request,
                                         special_index=user.user_cache.special_index,
                                         special_answers=[i.answer for i in user.answers],
                                         vk_id=user.vk_id)

        result = self.__parse_answer(result, user, current_menu)
        current_menu = result[1]
        user.delete_all_dinamic_items()
        for k, v in current_menu.items.items():
            if v[2] is not None:
                user.add_dinamic_items(index_name=k, dinamic_name=v[2](user_id=user.vk_id))
        return result
