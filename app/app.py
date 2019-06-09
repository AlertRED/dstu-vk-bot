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
        self.treatment = Controller(self.userDAO)
        self.vk = vk
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
        user = self.userDAO.first_or_create_user(from_id, vk_user[0]['first_name'], vk_user[0]['last_name'], root.name)
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


def get_format_place(name):
    place = placeDAO.get_place(name)
    if not place:
        return 'Извините, запрашевоемое место еще не добавлено'
    result = ''
    result += "Название: " + place.name + "\n"
    if place.adress:
        result += "Адрес: " + place.adress + "\n"
    if place.managers:
        result += "Управляющие: " + ''.join(i.first_name for i in place.managers) + "\n"
    if place.phones:
        result += "Телефоны: " + ' '.join(i.phone for i in place.phones) + "\n"
    if place.schedules:
        result += "Расписание: \n" + '\n'.join(
            '%s: %s - %s (перерыв %s - %s )' % (
                i.day_of_week.name, i.start_time.strftime("%H:%M"), i.end_time.strftime("%H:%M"),
                i.pause_start_time.strftime("%H:%M"), i.pause_end_time.strftime("%H:%M"))
            for i in place.schedules) + "\n"
    if place.map_url:
        result += "Карта: " + place.map_url + "\n"
    return result


def about_me(**kwargs):
    return "Я помогу узнать необходимую для тебя информацию о ДГТУ. " \
           "Помогу найти нужный корпус или узнать подробную информацию о стипендиях. " \
           "Спрашивай, не стисняйся!&#128521;"


root = Menu("Главное меню")

main_housing = Menu("Главный корпус")
asa_housing = Menu("АСА ДГТУ")

housings = Menu("Корпуса")
housings.add_basic_item("Главный корпус", "", lambda **kwargs: get_format_place(kwargs['request']))
housings.add_basic_item("Конгресс-холл", "", lambda **kwargs: get_format_place(kwargs['request']))
housings.add_basic_item("Корпус №2", "", lambda **kwargs: get_format_place(kwargs['request']))
housings.add_basic_item("Корпус №3,4,5", "", lambda **kwargs: get_format_place(kwargs['request']))
housings.add_basic_item("Корпус №6,7", "", lambda **kwargs: get_format_place(kwargs['request']))
housings.add_basic_item("Корпус №8", "", lambda **kwargs: get_format_place(kwargs['request']))

cafe_housings = Menu("Кафе")
cafe_housings.add_basic_item("Кафе «Экспресс»", "", lambda **kwargs: get_format_place(kwargs['request']))
cafe_housings.add_basic_item("Кафе «Русь»", "", lambda **kwargs: get_format_place(kwargs['request']))
cafe_housings.add_basic_item("Кафе «Миг»", "", lambda **kwargs: get_format_place(kwargs['request']))
cafe_housings.add_basic_item("Кафе «Миг»", "", lambda **kwargs: get_format_place(kwargs['request']))
cafe_housings.add_basic_item("Кафе «Кафедра»", "", lambda **kwargs: get_format_place(kwargs['request']))

hostels = Menu("Общажития")
hostels.add_basic_item("Общежитие №1", "", lambda **kwargs: get_format_place(kwargs['request']))
hostels.add_basic_item("Общежитие №2", "", lambda **kwargs: get_format_place(kwargs['request']))
hostels.add_basic_item("Общежитие №3", "", lambda **kwargs: get_format_place(kwargs['request']))
hostels.add_basic_item("Общежитие №4", "", lambda **kwargs: get_format_place(kwargs['request']))
hostels.add_basic_item("Общежитие №5", "", lambda **kwargs: get_format_place(kwargs['request']))

sport_housings = Menu("Спортивные комплексы")
sport_housings.add_basic_item("Легкоатлетический манеж", "", lambda **kwargs: get_format_place(kwargs['request']))
sport_housings.add_basic_item("Мини-футбольное поле", "", lambda **kwargs: get_format_place(kwargs['request']))
sport_housings.add_basic_item("Футбольное поле", "", lambda **kwargs: get_format_place(kwargs['request']))
sport_housings.add_basic_item("Бассейн", "", lambda **kwargs: get_format_place(kwargs['request']))

other = Menu("Другое")
other.add_basic_item("Храм св. мученицы Татианы", "", lambda **kwargs: get_format_place(kwargs['request']))
other.add_basic_item("Коворкинг «Gараж»", "", lambda **kwargs: get_format_place(kwargs['request']))
other.add_basic_item("Скейт-парк", "", lambda **kwargs: get_format_place(kwargs['request']))

main_housing.add_menu_item(housings.name, housings, True, "Назад")
main_housing.add_menu_item(cafe_housings.name, cafe_housings, True, "Назад")
main_housing.add_menu_item(hostels.name, hostels, True, "Назад")
main_housing.add_menu_item(sport_housings.name, sport_housings, True, "Назад")
main_housing.add_menu_item(other.name, other, True, "Назад")

root.add_menu_item(main_housing.name, main_housing, True, "Назад")
root.add_menu_item(asa_housing.name, asa_housing, True, "Назад")

root.add_basic_item("Рассакажи о себе", "", about_me)
