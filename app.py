import json
import time

from sqlalchemy.orm import Session
from vk_api import VkApi

from menues import Menu
from scratch import Treatment
from user_dao import userDAO
import random
import logging


class app:

    def __init__(self, db: Session, vk: VkApi):
        self.db = db
        self.userDAO = userDAO(self.db)
        self.treatment = Treatment(self.userDAO)
        self.vk = vk
        logging.basicConfig(filename="history.log", level=logging.INFO)

    def get_button(self, label, color, payload=""):
        return {
            "action": {
                "type": "text",
                "payload": json.dumps(payload),
                "label": label
            },
            "color": color
        }

    def get_keyboard(self, labels: list):

        buttons = []
        for i in range(0, len(labels), 4):
            buttons.append([self.get_button(label=label, color="primary") for label in labels[i:i + 4]])

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
                            "random_id": random.randint(1, 2147483647)})
        if menu:
            self.vk.method("messages.send",
                           {"peer_id": id_user, "message": menu.get_menu(),
                            "keyboard": self.get_keyboard([i for i in menu.items.keys()]),
                            "random_id": random.randint(1, 2147483647)})

    # def log(self, foo):
    #     def log_foo(from_id: int, text: str):
    #         logging.info('')
    #         result = foo(from_id, text)
    #         logging.info('')
    #     return log_foo(from_id, text)
    #
    # @log
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
                time.sleep(1)



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

def grant_government():
    return 'Cnипендию могут получить следующие лица:\n'\
           ' - Cтуденты, проходящие обучение очно, в учреждении среднего профессионального образования\n'\
           ' - Cтуденты и аспиранты, учащиеся на очной форме, в высшем учебном заведении.\n' \
           '\nУсловия получения' \
           ' - По результатам семестра у претендента не должно быть оценок «удовлетворительно» по экзаменам и зачетам. При этом оценок «отлично» должно быть не меньше половины от общего числа;\n' \
           ' - Систематическое участие или победа в состязаниях и конкурсах разного уровня, от регионального до международного. У кандидата должно быть подтверждение данных достижений в документальном виде. Эти успехи оцениваются за полтора года до подачи заявки;\n' \
           ' - Систематическое участие в научной, исследовательской или технико-конструкторской деятельности учебного заведения в течение периода не менее полутора лет до подачи заявки.\n' \
           '\nРазмер стипендии:\n' \
           'Размер в среднем составляет 3500 руб. для учащихся в ВУЗах.'

def grant_basic():
    return 'Условия получения:' \
           ' - Сдать промежуточную аттестацию на «отлично»\n' \
           ' - Сдать промежуточную аттестацию на «хорошо» и «отлично»\n' \
           ' - Сдать промежуточную аттестацию на «хорошо»\n' \
           ' - Сдать промежуточную аттестацию не в установленный срок\n' \
           ' - Иностранные граждане, сдавшие промежуточную аттестацию на «удовлетворительно» или имеющие задолженность\n' \
           ' - Студенты, поступившие на 1 курс 1 семестра\n' \
           '\nРазмеры стипендии:' \
           'на «отлично» - 3500\n' \
           'на «хорошо» и «отлично» - 3100\n' \
           'на «хорошо» - 2700\n' \
           'не в установленный срок – 1600\n' \
           'иностранным гражданам – 1600\n' \
           '1 курс 1 семестр – 1600'

def grant_governor():
    return 'Условия: \n' \
           ' - Учащийся обязан проявить особые способности в учебной и научной деятельности как в целом по курсу обучения, так и по отдельным дисциплинам\n' \
           ' - Учащийся должен быть жителем Ростовской области\n' \
           'Размер:\n' \
           'Размер в среднем составляет 2000 руб. для учащихся в ВУЗах.\n' \
           'Стипендия присвоена 40 лучшим аспирантам и адъюнктам, 150 студентам и курсантам вузов. Из них 41 человек обучается в Донском государственном техническом университете.\n' \

root = Menu("Главное меню")
menu_housing = Menu("&#127970;Корпуса")

menu_housing.add_item("1", "Главный корпус", main_corp)
menu_housing.add_item("2", "Корпус №2", corp_2)
menu_housing.add_item("3", "Корпус №3", corp_3)
menu_housing.add_item("4", "Корпус №4", corp_4)
menu_housing.add_item("5", "Корпус №5", corp_5)
menu_housing.add_item("6", "Корпус №8", corp_8)

root.add_menu("1", menu_housing, True)

menu_grant = Menu("&#128179;Стипендии")
menu_grant.add_item("1", "Правительственная", grant_government)
menu_grant.add_item("2", "Губернаторская", grant_governor)
menu_grant.add_item("3", "Обычная", grant_basic)

root.add_menu("2", menu_grant, True)

root.add_item("3", "&#128483;Рассакажи о себе", about_me)
