import json

from sqlalchemy.orm import Session
from vk_api import VkApi

from app.menues import Menu, TypeItem
from app.scratch import Treatment
from app.user_dao import userDAO
import random
import logging


class app:

    def __init__(self, db: Session, vk: VkApi):
        self.db = db
        self.userDAO = userDAO(self.db)
        self.treatment = Treatment(self.userDAO)
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
            try:
                messages = self.vk.method("messages.getConversations",
                                          {"offset": 0, "count": 20, "filter": "unanswered"})
                if messages["count"] >= 1:
                    id = messages["items"][0]["last_message"]["from_id"]
                    body = messages["items"][0]["last_message"]["text"]
                    self.receive_message(id, body)
            except Exception as E:
                logging.error(E)
                # time.sleep(1)


def main_corp():
    return "Главный корпус\n" \
           "📌 пл. Гагарина 1 \n" \
           "📞 (863) 273-85-45\n" \
           "https://www.google.ru/maps/place/%D0%BF%D1%80.+%D0%9C%D0%B8%D1%85%D0%B0%D0%B8%D0%BB%D0%B0+%D0%9D%D0%B0%D0%B3%D0%B8%D0%B1%D0%B8%D0%BD%D0%B0,+1,+%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2-%D0%BD%D0%B0-%D0%94%D0%BE%D0%BD%D1%83,+%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F+%D0%BE%D0%B1%D0%BB.,+344000/@47.2372611,39.7116583,19z/data=!3m1!4b1!4m12!1m6!3m5!1s0x40e3bbd25efc8dab:0xe71795934da757ba!2z0JTQk9Ci0KM!8m2!3d47.2373015!4d39.7121356!3m4!1s0x40e3b9ac0bc4e667:0x80a7625a92585ed5!8m2!3d47.2372602!4d39.7122076"


def holl():
    return "Конгресс-холл\n" \
           "📌 пл. Гагарина 1\n" \
           "📞 (863) 238-17-29\n"


def corp_2():
    return "Корпус № 2\n" \
           "📌 пл. Гагарина 1" \
           "📞 (863) 273-87-57\n" \
           "https://www.google.ru/maps/place/%D0%9E%D0%9E%D0%9E+%22%D0%AD%D0%BD%D1%81%D0%B5%D1%82%22/@47.2377351,39.7109535,18.03z/data=!4m12!1m6!3m5!1s0x40e3bbd25efc8dab:0xe71795934da757ba!2z0JTQk9Ci0KM!8m2!3d47.2373015!4d39.7121356!3m4!1s0x40e3b9ac4331b98d:0xaafa5d8cce7b6706!8m2!3d47.2385613!4d39.7130227"


def corp_3_4_5():
    return "Корпус № 3,4,5\n" \
           "📌 пл. Гагарина 1\n" \
           "📞 (863) 273-84-46\n" \
           "https://www.google.ru/maps/place/%D0%A3%D1%87%D0%B5%D0%B1%D0%BD%D0%BE-%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D1%8B%D0%B5+%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81%D0%B0+%E2%84%96+3,+4,+5/@47.2382094,39.7102012,18z/data=!4m5!3m4!1s0x40e3b9ac9c54d9e3:0x92d4fa6c4ce0e552!8m2!3d47.2383323!4d39.7095948"


def corp_6_7():
    return "Корпус № 6,7\n" \
           "📌 пл. Гагарина 1\n" \
           "📞 (863) 273-87-57\n" \
           ""


def corp_8():
    return "Корпус № 8\n" \
           "📌 пл. Гагарина 1\n" \
           "📞 (863) 238-13-15 (карта)\n" \
           "https://www.google.ru/maps/place/%D0%A3%D1%87%D0%B5%D0%B1%D0%BD%D0%BE-%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D1%8B%D0%B9+%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81+%E2%84%96+8/@47.2377068,39.7112081,18.33z/data=!4m12!1m6!3m5!1s0x40e3bbd25efc8dab:0xe71795934da757ba!2z0JTQk9Ci0KM!8m2!3d47.2373015!4d39.7121356!3m4!1s0x40e3b9ac7dc21d41:0x7718a6501d7dfc82!8m2!3d47.2380108!4d39.7109641"


def about_me():
    return "Я помогу узнать необходимую для тебя информацию о ДГТУ. " \
           "Помогу найти нужный корпус или узнать подробную информацию о стипендиях. " \
           "Спрашивай, не стисняйся!&#128521;"


root = Menu("Главное меню")

main_housing = Menu("Главный корпус")
asa_housing = Menu("АСА ДГТУ")

housings = Menu("Корпуса")
housings.add_basic_item("Главный корпус", "", main_corp)
housings.add_basic_item("Конгресс-холл", "", holl)
housings.add_basic_item("Корпус №2", "", corp_2)
housings.add_basic_item("Корпус №3,4,5", "", corp_3_4_5)
housings.add_basic_item("Корпус №6,7", "", corp_6_7)
housings.add_basic_item("Корпус №8", "", corp_8)

cafe_housings = Menu("Кафе")
cafe_housings.add_basic_item("Кафе «Экспресс»", "", lambda: "Кафе «Экспресс» - 🕘 пн.-пт. | 8.30 – 17.00 |\n"
                                                            "📌 Корпус №8 (цоколь)")
cafe_housings.add_basic_item("Кафе «Русь»", "", lambda: "Кафе «Русь» - 🕘 пн.-пт. | 8.30 – 18.00 |\n"
                                                        "📌 ул. Текучева 145")
cafe_housings.add_basic_item("Кафе «Миг»", "", lambda: "Кафе «Миг» - 🕘 пн.-пт. | 8.30 – 17.00 |\n"
                                                       "📌 Главный корпус (2-й этаж)")
cafe_housings.add_basic_item("Кафе «Миг»", "", lambda: "Кафе «Миг» - 🕘 пн.-пт. | 8.30 – 17.00 |\n"
                                                       "📌 Главный корпус (2-й этаж) (карта)")
cafe_housings.add_basic_item("Кафе «Кафедра»", "", lambda: "Кафе «Кафедра» - 🕘 пн.-пт. | 8.30 – 17.00 |\n"
                                                           "📌 Корпус №7 (1-й этаж) (карта)")

hostels = Menu("Общажития")
hostels.add_basic_item("Общежитие №1", "", lambda: "Общежитие №1 - 👤Дарсания Лемин Бичикоевич\n"
                                                   "📌 ул. Студенческая 2 \n"
                                                   "📞 (863) 211-10-41, 252-15-78")
hostels.add_basic_item("Общежитие №2", "", lambda: "Общежитие №2 - 👤Тугуши Давид Александрович\n"
                                                   "📌 пр. М. Нагибина 5 \n"
                                                   "📞 (863) 273-84-18, 232-78-93")
hostels.add_basic_item("Общежитие №3", "", lambda: "Общежитие №3 - 👤Исраилов Султан Адамович\n"
                                                   "📌 ул. Мечникова 79а \n"
                                                   "📞 (863) 273-84-19, 273-87-06")
hostels.add_basic_item("Общежитие №4", "", lambda: "Общежитие №4 - 👤Газиев Руслан Яхьяевич\n"
                                                   "📌 ул. Текучева 145\n"
                                                   "📞 (863) 273-87-10, 273-87-10")
hostels.add_basic_item("Общежитие №5", "", lambda: "Общежитие №5 - 👤Тугуши Давид Александрович\n"
                                                   "📌 пр. М. Нагибина 5\n"
                                                   "📞 (863) 211-10-41, 252-15-78")

sport_housings = Menu("Спортивные комплексы")
sport_housings.add_basic_item("Легкоатлетический манеж", "", lambda: "Легкоатлетический манеж")
sport_housings.add_basic_item("Мини-футбольное поле", "", lambda: "Мини-футбольное поле")
sport_housings.add_basic_item("Футбольное поле", "", lambda: "Футбольное поле")
sport_housings.add_basic_item("Бассейн", "", lambda: "Бассейн")

other = Menu("Другое")
other.add_basic_item("Храм св. мученицы Татианы", "", lambda: "Храм св. мученицы Татианы")
other.add_basic_item("Коворкинг «Gараж»", "", lambda: "Легкоатлетический манеж")
other.add_basic_item("Скейт-парк", "", lambda: "Скейт-парк")

main_housing.add_menu_item(housings.name, housings, True, "Назад")
main_housing.add_menu_item(cafe_housings.name, cafe_housings, True, "Назад")
main_housing.add_menu_item(hostels.name, hostels, True, "Назад")
main_housing.add_menu_item(sport_housings.name, sport_housings, True, "Назад")
main_housing.add_menu_item(other.name, other, True, "Назад")

root.add_menu_item(main_housing.name, main_housing, True, "Назад")
root.add_menu_item(asa_housing.name, asa_housing, True, "Назад")

root.add_basic_item("Рассакажи о себе", "", about_me)
# menu_housing = Menu("Корпуса")
#
# menu_housing.add_item("Главный корпус", "", main_corp)
# menu_housing.add_item("Корпус №2", "", corp_2)
# menu_housing.add_item("Корпус №3", "", corp_3)
# menu_housing.add_item("Корпус №4", "", corp_4)
# menu_housing.add_item("Корпус №5", "", corp_5)
# menu_housing.add_item("Корпус №8", "", corp_8)
#
# root.add_menu(menu_housing.name, menu_housing, True)
# root.add_item("Рассакажи о себе", "", about_me)
