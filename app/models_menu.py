from enum import Enum


class TypeItem(Enum):
    BACK = 1
    MENU = 2
    SIMPLE = 3
    GATE = 4


class Item:

    def __init__(self, name: str, method):
        self.name = name
        self.method = method

    def call(self, *args, **kwargs):
        return {"answer": self.method(**kwargs), "new_menu": None}


class Menu(Item):
    menues: list = []

    def __init__(self, name, method=None):
        super().__init__(name, None)
        self.name = name
        self.method = method
        self.parent = None
        self.items = {}
        Menu.menues.append(self)
        self.index = len(Menu.menues) - 1

    def get_menu(self):
        return " > ".join(reversed(["[ %s ]" % i for i in self.get_story()]))

    def call(self, *args, **kwargs):
        return {"answer": self.method(*args, **kwargs) if self.method else None, "new_menu": self}

    # получить ответ от меню
    def get_answer(self, request, *args, **kwargs):
        result = self.items.get(request, None)
        return result[0].call(*args, **kwargs, request=request) if result else self.call(*args, **kwargs,
                                                                                         request=request)

    def _add_item(self, index, item_of_menu, type_item: TypeItem = TypeItem.GATE):
        self.items[index] = item_of_menu, type_item
        if self.items.get('Назад'):
            self.items['Назад'] = self.items.pop('Назад')


    # добавить пункт меню
    def add_basic_item(self, index, name, method, type_item: TypeItem = TypeItem.SIMPLE):
        self._add_item(index, Item(name, method), type_item)

    # добавить пункт меню
    def add_special_item(self, index, name, messages: list, method, is_back=True, back_point_text="Назад",
                         type_item: TypeItem = TypeItem.SIMPLE, prepare=None):
        special = SpecialMenu(name, messages, method, self)
        if prepare is not None:
            special.prepare_condition = prepare['condition']
            special.prepare_method = prepare['method']
        self._add_item(index, special, type_item)
        if is_back:
            special.add_back_point(special.parent, back_point_text)

    # добавить вложенное меню
    def add_menu_item(self, index, menu, is_back=True, back_point_text="Назад", type_item: TypeItem = TypeItem.MENU):
        self._add_item(index, menu, type_item)
        menu.parent = self
        if is_back:
            menu.add_back_point(menu.parent, back_point_text)

    def add_back_point(self, menu, back_point_text: str):
        name_back_button = back_point_text if back_point_text else menu.name
        self._add_item(name_back_button, menu, TypeItem.BACK)

    def get_story(self):
        menu = self
        result = []
        while menu:
            result.append(menu.name)
            menu = menu.parent
        return result


class SpecialMenu(Menu):

    def __init__(self, name: str, messages: list, method, parent=None):
        super().__init__(name)
        self.messages = messages
        self.parent = parent
        self.method = method
        self.prepare_condition = None
        self.prepare_method = None

    def get_answer(self, request, *args, **kwargs):
        result = self.items.get(request, None)
        answer = result[0].call(*args, **kwargs, request=request) if result else self.call(*args, **kwargs,
                                                                                           request=request)
        if result and result[1] is TypeItem.BACK:
            answer['special_index'] = 0
            answer['special_answers'] = []
        return answer

    def is_end(self, number: int):
        return (len(self.messages) - 1) < number

    def prepare(self, *args, **kwargs):
        return self.prepare_condition and self.prepare_method and self.prepare_condition(*args, **kwargs)

    def call(self, *args, **kwargs):

        if self.prepare(*args, **kwargs):
            return {
                'answer': self.prepare_method(*args, **kwargs),
                'new_menu': self.parent,
                'special_index': 0
            }

        index_answer = kwargs.get('special_index', 0)
        list_answers = kwargs.get('special_answers')

        if index_answer > 0:
            list_answers.append(kwargs.get('request'))

        if self.is_end(index_answer):
            return {"answer": self.method(list_answers=list_answers, vk_id=kwargs.get('vk_id', None)),
                    "new_menu": self.parent,
                    "special_index": 0}

        return {"answer": self.messages[index_answer],
                "new_menu": self,
                "special_index": index_answer + 1,
                "special_answers": list_answers}
