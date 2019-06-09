from enum import Enum


class TypeItem(Enum):
    BACK = 1
    MENU = 2
    SIMPLE = 3
    DEFAULT = 4


class Item:

    def __init__(self, name: str, method):
        self.name = name
        self.method = method

    def call(self, *args, **kwargs):
        return {"answer": self.method(**kwargs), "new_menu": None}


class Menu(Item):
    menues: dict = {}
    back_point_text = ""

    def __init__(self, name):
        super().__init__(name, None)
        self.name = name
        self.parent: Menu = None
        self.items = {}
        Menu.menues[self.name] = self

    def get_menu(self):
        text_menu = " > ".join(reversed(["[ %s ]" % i for i in self.get_story()]))
        # text_menu += "\n".join(
        #     ["%s. %s" % (key, node.name) for key, node in self.items.items()])
        return text_menu

    def call(self, *args, **kwargs):
        return {"answer": None, "new_menu": self}

    # получить ответ от меню
    def get_answer(self, request, *args, **kwargs):
        result = self.items.get(request, None)
        return result[0].call(*args, **kwargs, request=request) if result else self.call(*args, **kwargs, request=request)

    def _add_item(self, index, item, type_item: TypeItem = TypeItem.DEFAULT):
        self.items[index] = item, type_item

    # добавить пункт меню
    def add_basic_item(self, index, name, method, type_item: TypeItem = TypeItem.SIMPLE):
        self._add_item(index,Item(name, method), type_item)

    # добавить пункт меню
    def add_special_item(self, index, name, messages: list, method, type_item: TypeItem = TypeItem.SIMPLE):
        special = SpecialMenu(name, messages, method)
        special.parent = self
        self._add_item(index, special, type_item)


    # добавить вложенное меню
    def add_menu_item(self, index, menu, is_back=False, back_point_text="", type_item: TypeItem = TypeItem.MENU):
        self.items[index] = [menu, type_item]
        menu.parent = self
        if is_back:
            menu.add_back_point(menu.parent, back_point_text)

    def add_back_point(self, menu, back_point_text):
        index = back_point_text if back_point_text else menu.name
        self._add_item(index, menu, TypeItem.BACK)

    def get_story(self):
        menu = self
        result = []
        while menu:
            result.append(menu.name)
            menu = menu.parent
        return result


class SpecialMenu(Menu):

    def __init__(self, name: str, messages: list, method):
        super().__init__(name)
        self.messages = messages
        self.parent = None
        self.method = method

    def is_end(self, number):
        return number and ((len(self.messages) - 1) < number)

    def call(self, *args, **kwargs):
        number = kwargs.get('special_index', 0)
        lst = kwargs.get('special_answers')
        if number and number > 0:
            lst.append(kwargs.get('request'))

        if self.is_end(number):
            answer = self.method(lst)
            new_menu = self.parent
            number = 0
            lst = []
        else:
            answer = self.messages[number]
            new_menu = self
            number += 1
        return {"answer": answer, "new_menu": new_menu, "special_index": number, "special_answers": lst}

# sub_menu = Menu("Вложенное меню")
# sub_menu.add_item("1", "Скажи привет еще раз", lambda: "Привет еще раз")
# root.add_menu("2", sub_menu, True)
# root.add_special("3", "Возвести в степень", ["Введите число: ", "Введите степень: "],
#                  lambda lst: int(lst[0]) ** int(lst[1]))
# root.add_special("4", "Сумма 5 чисел",
#                  ["Введите число: ", "Введите число: ", "Введите число: ", "Введите число: ", "Введите число: "],
#                  lambda lst: sum([int(i) for i in lst]))

# class User:
#     current_menu: Menu = root
#     special_index = 0  # текущий пункт специального меню
#     special_question = None  # вопрос специального меню
#     special_answers = []  # накопленные ответы на вопросы


# if __name__ == '__main__':
#     user = User()
#
#     print(user.current_menu.get_menu())
#     while True:
#         request = input('command: ' if not (type(user.current_menu) is SpecialMenu) else user.special_question)
#         result = user.current_menu.get_answer(request, special_index=user.special_index,
#                                               special_answers=user.special_answers)
#
#         answer = result.get("answer", None)
#         new_menu = result.get("new_menu", None)
#
#         if type(user.current_menu) is SpecialMenu:
#             user.special_answers = result.get("special_answers")
#             user.special_index = result.get("special_index", None)
#         elif type(new_menu) is SpecialMenu:
#             user.special_index = result.get("special_index", None)
#
#         if new_menu:
#             user.current_menu = new_menu
#
#         if type(user.current_menu) is SpecialMenu:
#             user.special_question = answer
#         else:
#             if answer:
#                 print(answer)
#             print(user.current_menu.get_menu())
