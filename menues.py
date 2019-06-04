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


def main_corp():
    return "https://www.google.ru/maps/place/%D0%BF%D1%80.+%D0%9C%D0%B8%D1%85%D0%B0%D0%B8%D0%BB%D0%B0+%D0%9D%D0%B0%D0%B3%D0%B8%D0%B1%D0%B8%D0%BD%D0%B0,+1,+%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2-%D0%BD%D0%B0-%D0%94%D0%BE%D0%BD%D1%83,+%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F+%D0%BE%D0%B1%D0%BB.,+344000/@47.2372611,39.7116583,19z/data=!3m1!4b1!4m12!1m6!3m5!1s0x40e3bbd25efc8dab:0xe71795934da757ba!2z0JTQk9Ci0KM!8m2!3d47.2373015!4d39.7121356!3m4!1s0x40e3b9ac0bc4e667:0x80a7625a92585ed5!8m2!3d47.2372602!4d39.7122076"


def corp_2():
    return "https://www.google.ru/maps/place/%D0%9E%D0%9E%D0%9E+%22%D0%AD%D0%BD%D1%81%D0%B5%D1%82%22/@47.2377351,39.7109535,18.03z/data=!4m12!1m6!3m5!1s0x40e3bbd25efc8dab:0xe71795934da757ba!2z0JTQk9Ci0KM!8m2!3d47.2373015!4d39.7121356!3m4!1s0x40e3b9ac4331b98d:0xaafa5d8cce7b6706!8m2!3d47.2385613!4d39.7130227"


def corp_4():
    return "https://www.google.ru/maps/place/%D0%A3%D1%87%D0%B5%D0%B1%D0%BD%D0%BE-%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D1%8B%D0%B5+%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81%D0%B0+%E2%84%96+3,+4,+5/@47.2382094,39.7102012,18z/data=!4m5!3m4!1s0x40e3b9ac9c54d9e3:0x92d4fa6c4ce0e552!8m2!3d47.2383323!4d39.7095948"


def corp_5():
    return "https://www.google.ru/maps/place/%D0%A3%D1%87%D0%B5%D0%B1%D0%BD%D0%BE-%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D1%8B%D0%B5+%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81%D0%B0+%E2%84%96+3,+4,+5/@47.2382094,39.7102012,18z/data=!4m5!3m4!1s0x40e3b9ac9c54d9e3:0x92d4fa6c4ce0e552!8m2!3d47.2383323!4d39.7095948"


def corp_3():
    return "https://www.google.ru/maps/place/%D0%A3%D1%87%D0%B5%D0%B1%D0%BD%D0%BE-%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D1%8B%D0%B5+%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81%D0%B0+%E2%84%96+3,+4,+5/@47.2382094,39.7102012,18z/data=!4m5!3m4!1s0x40e3b9ac9c54d9e3:0x92d4fa6c4ce0e552!8m2!3d47.2383323!4d39.7095948"


def corp_8():
    return "https://www.google.ru/maps/place/%D0%A3%D1%87%D0%B5%D0%B1%D0%BD%D0%BE-%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D1%8B%D0%B9+%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81+%E2%84%96+8/@47.2377068,39.7112081,18.33z/data=!4m12!1m6!3m5!1s0x40e3bbd25efc8dab:0xe71795934da757ba!2z0JTQk9Ci0KM!8m2!3d47.2373015!4d39.7121356!3m4!1s0x40e3b9ac7dc21d41:0x7718a6501d7dfc82!8m2!3d47.2380108!4d39.7109641"


def about_me():
    return "Я помогу узнать необходимую для тебя информацию о ДГТУ. " \
           "Помогу найти нужный корпус или узнать подробную информацию о стипендиях. " \
           "Спрашивай, не стисняйся!&#128521;"


root = Menu("Главное меню")
root.add_item("1", "Главный корпус", lambda: main_corp)
root.add_item("2", "Корпус №2", lambda: corp_2)
root.add_item("3", "Корпус №2", lambda: corp_3)
root.add_item("4", "Корпус №2", lambda: corp_4)
root.add_item("5", "Корпус №4", lambda: corp_5)
root.add_item("6", "Корпус №8", lambda: corp_8)
root.add_item("7", "Рассакажи о себе", about_me)


# sub_menu = Menu("Вложенное меню")
# sub_menu.add_item("1", "Скажи привет еще раз", lambda: "Привет еще раз")
# root.add_menu("2", sub_menu, True)
# root.add_special("3", "Возвести в степень", ["Введите число: ", "Введите степень: "],
#                  lambda lst: int(lst[0]) ** int(lst[1]))
# root.add_special("4", "Сумма 5 чисел",
#                  ["Введите число: ", "Введите число: ", "Введите число: ", "Введите число: ", "Введите число: "],
#                  lambda lst: sum([int(i) for i in lst]))

class User:
    current_menu: Menu = root
    special_index = 0  # текущий пункт специального меню
    special_question = None  # вопрос специального меню
    special_answers = []  # накопленные ответы на вопросы


if __name__ == '__main__':
    user = User()

    print(user.current_menu.get_menu())
    while True:
        request = input('command: ' if not (type(user.current_menu) is SpecialMenu) else user.special_question)
        result = user.current_menu.get_answer(request, special_index=user.special_index,
                                              special_answers=user.special_answers)

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
