class Item:

    def __init__(self, name: str, method):
        self.name = name
        self.method = method

    def call(self, *args, **kwargs):
        return {"answer": self.method(), "new_menu": None}


class Menu(Item):
    menues: dict = {}

    def __init__(self, name):
        super().__init__(name, None)
        self.name = name
        self.parent: Menu = None
        self.items = {}
        Menu.menues[self.name] = self

    def get_menu(self):
        text_menu = " > ".join(reversed(["[ %s ]" % i for i in self.get_story()])) + "\n"
        text_menu += "\n".join(
            ["%s. %s" % (key, node.name) for key, node in self.items.items()])
        return text_menu

    def call(self, *args, **kwargs):
        return {"answer": None, "new_menu": self}

    # получить ответ от меню
    def get_answer(self, request, *args, **kwargs):
        result = self.items.get(request, None)
        return result.call(*args, **kwargs, request=request) if result else self.call(*args, **kwargs, request=request)

    # добавить пункт меню
    def add_item(self, index, name, method):
        self.items[index] = Item(name, method)

    # добавить пункт меню
    def add_special(self, index, name, messages: list, method):
        special = SpecialMenu(name, messages, method)
        special.parent = self
        self.items[index] = special

    # добавить вложенное меню
    def add_menu(self, index, menu, is_back=False):
        self.items[index] = menu
        menu.parent = self
        if is_back:
            menu.add_back_point(menu.parent)

    def add_back_point(self, menu):
        self.items["0"] = menu

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


root = Menu("Главное меню")
root.add_item("1", "Скажи привет", lambda: "Привет")

sub_menu = Menu("Вложенное меню")
sub_menu.add_item("1", "Скажи привет еще раз", lambda: "Привет еще раз")
root.add_menu("2", sub_menu, True)
root.add_special("3", "Возвести в степень", ["Введите число: ", "Введите степень: "],
                 lambda lst: int(lst[0]) ** int(lst[1]))
root.add_special("4", "Сумма 5 чисел",
                 ["Введите число: ", "Введите число: ", "Введите число: ", "Введите число: ", "Введите число: "],
                 lambda lst: sum([int(i) for i in lst]))

class User:
    current_menu: Menu = root
    special_index = 0 # текущий пункт специального меню
    special_question = None # вопрос специального меню
    special_answers = [] # накопленные ответы на вопросы

if __name__ == '__main__':
    user = User()

    print(user.current_menu.get_menu())
    while True:
        request = input('command: ' if not (type(user.current_menu) is SpecialMenu) else user.special_question)
        result = user.current_menu.get_answer(request, special_index=user.special_index, special_answers=user.special_answers)

        answer = result.get("answer", None)
        new_menu = result.get("new_menu", None)

        if type(user.current_menu) is SpecialMenu:
            user.special_answers = result.get("special_answers")
            user.special_index = result.get("special_index", None)
        elif type(new_menu) is SpecialMenu:
            user.special_index = result.get("special_index", None)

        if new_menu:
            user.current_menu = new_menu

        if type(user.current_menu) is SpecialMenu:
            user.special_question = answer
        else:
            if answer:
                print(answer)
            print(user.current_menu.get_menu())
