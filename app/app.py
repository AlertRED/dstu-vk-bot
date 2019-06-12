import json

from sqlalchemy.orm import Session
from vk_api import VkApi

from app.menues import Menu, TypeItem
from app.controller import Controller
from app.user_dao import userDAO
from app.place_dao import placeDAO
import random
import logging


class app:

    def __init__(self, db: Session, vk: VkApi):
        self.db = db
        self.userDAO = userDAO(self.db)
        self.placeDAO = placeDAO(self.db)
        self.treatment = Controller(self.userDAO)
        self.vk = vk

        self.create_menues()

        logging.basicConfig(filename="config/history.log", level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='[%m-%d-%Y %I:%M:%S]')


    def get_button(self, label, color, payload=""):
        return {
            "action": {
                "type": "text",
                "payload": json.dumps(payload),
                "label": label
            },
            "color": color
        }

    def get_keyboard(self, items: dict):
        buttons = []
        group = []

        colors = {TypeItem.DEFAULT: 'default',
                  TypeItem.BACK: 'negative',
                  TypeItem.MENU: 'positive',
                  TypeItem.SIMPLE: 'primary'}

        for label, obj in items.items():
            limit = 30 // (len(group) + 1)
            group.append((label, colors.get(obj[1], "default")))
            if any(map(lambda x: len(x[0]) > limit, group)) or (len(group) > 4):
                buttons.append(list(map(lambda i: self.get_button(label=i[0], color=i[1]), group[:-1])))
                group = group[-1:]
        else:
            buttons.append(list(map(lambda i: self.get_button(label=i[0], color=i[1]), group)))

        keyboard = {
            "one_time": True,
            "buttons": buttons
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        return str(keyboard.decode('utf-8'))



    def send_message(self, answer, menu, id_user):
        if answer:
            self.vk.method("messages.send",
                           {"peer_id": id_user,
                            "message": answer,
                            "keyboard": self.get_keyboard(menu.items),
                            "random_id": random.randint(1, 2147483647)})
        elif menu:
            self.vk.method("messages.send",
                           {"peer_id": id_user, "message": menu.name,
                            "keyboard": self.get_keyboard(menu.items),
                            "random_id": random.randint(1, 2147483647)})

    def receive_message(self, from_id: int, text: str):
        logging.info("From id: %d, message: %s" % (from_id, text))
        vk_user = self.vk.method("users.get", values={"user_ids": from_id})
        user = self.userDAO.first_or_create_user(from_id, vk_user[0]['first_name'], vk_user[0]['last_name'], self.root.name)
        self.userDAO.user_inc_request(user.vk_id)
        answer, menu = self.treatment.get_answer(text, user)
        self.send_message(answer, menu, from_id)
        return answer, menu

    def run(self):
        while True:
            # try:
            messages = self.vk.method("messages.getConversations",
                                      {"offset": 0, "count": 20, "filter": "unanswered"})
            if messages["count"] >= 1:
                id = messages["items"][0]["last_message"]["from_id"]
                body = messages["items"][0]["last_message"]["text"]
                self.receive_message(id, body)
            # except Exception as E:
            #     logging.error(E)
            #     # time.sleep(1)

    def get_format_place(self, name):
        place = self.placeDAO.get_place_by_name(name)
        if not place:
            return 'Извините, запрашевоемое место еще не добавлено'
        result = ''
        result += "Название: " + place.name + "\n"
        if place.adress:
            result += "📍Адрес: " + place.adress + "\n"
        if place.managers:
            result += "👤Управляющие: " + ''.join(i.first_name for i in place.managers) + "\n"
        if place.phones:
            result += "📞Телефоны: " + ', '.join(i.phone for i in place.phones)+"\n"
        if place.schedules:
            result += "🕗Расписание: \n" + '\n'.join(
                '%s: %s - %s' % (
                    i.day_of_week.name, i.start_time.strftime("%H:%M"), i.end_time.strftime("%H:%M"))
                for i in place.schedules) + "\n"
        if place.map_url:
            result += "Карта: " + place.map_url + "\n"
        return result

    def get_place_menu(self, button_name: str, place_type: str):
        menu = Menu(button_name)
        for place in self.placeDAO.get_place_by_type(place_type):
            menu.add_basic_item(place.name, "", lambda **kwargs: self.get_format_place(kwargs['request']))
        return menu

    def create_menues(self):
        self.root = Menu("Главное меню")
        self.asa_housing = Menu("АСА ДГТУ")
        self.main_housing = Menu("Корпус ДГТУ")

        self.housings = self.get_place_menu('Корпуса', 'Корпус')
        self.cafe_housings = self.get_place_menu('Кафе', 'Кафе')
        self.hostels = self.get_place_menu('Общежития', 'Общежитие')
        self.sport_housings = self.get_place_menu('Спортивные комплексы', 'Спортивные комплексы')
        self.other = self.get_place_menu('Другое', 'Другое')

        self.main_housing.add_menu_item(self.housings.name, self.housings, True, "Назад")
        self.main_housing.add_menu_item(self.cafe_housings.name, self.cafe_housings, True, "Назад")
        self.main_housing.add_menu_item(self.hostels.name, self.hostels, True, "Назад")
        self.main_housing.add_menu_item(self.sport_housings.name, self.sport_housings, True, "Назад")
        self.main_housing.add_menu_item(self.other.name, self.other, True, "Назад")

        self.root.add_menu_item(self.main_housing.name, self.main_housing, True, "Назад")
        self.root.add_menu_item(self.asa_housing.name, self.asa_housing, True, "Назад")

        self.root.add_basic_item("Рассакажи о себе", "", self.about_me)


    def about_me(self, **kwargs):
        return "Я помогу узнать необходимую для тебя информацию о ДГТУ. " \
               "Помогу найти нужный корпус или узнать подробную информацию о стипендиях. " \
               "Спрашивай, не стисняйся!&#128521;"


