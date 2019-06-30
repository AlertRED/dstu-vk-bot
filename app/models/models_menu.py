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

    def __init__(self, name):
        super().__init__(name, None)
        self.name = name
        self.parent = None
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
    def add_menu_item(self, index, menu, is_back=True, back_point_text="Назад", type_item: TypeItem = TypeItem.MENU):
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

    def is_end(self, number: int):
        return (len(self.messages) - 1) < number

    def call(self, *args, **kwargs):
        index_answer = kwargs.get('special_index', 0)
        list_answers = kwargs.get('special_answers')
        if index_answer > 0:
            list_answers.append(kwargs.get('request'))

        if self.is_end(index_answer):
            return {"answer": self.method(list_answers),
                    "new_menu": self.parent,
                    "special_index": 0}
        else:
            return {"answer": self.messages[index_answer],
                    "new_menu": self,
                    "special_index": index_answer+1,
                    "special_answers": list_answers}
