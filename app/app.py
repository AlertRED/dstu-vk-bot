import json
import os

from sqlalchemy.orm import Session
from vk_api import VkApi, VkUpload

from app.menues import MenuTree
from app.models.models_menu import TypeItem
from app.controller import Controller
# from app.daos.user_dao import userDAO
from app.models.models import User
import random
import logging


class app:

    def __init__(self, db: Session, vk: VkApi, vk_upload: VkUpload):
        self.colors = {TypeItem.DEFAULT: 'default',
                       TypeItem.BACK: 'negative',
                       TypeItem.MENU: 'positive',
                       TypeItem.SIMPLE: 'primary'}

        self.db = db
        # self.userDAO = userDAO()
        self.controller = Controller()
        self.vk = vk
        self.vk_upload = vk_upload
        self.images_dir = os.path.join(os.getcwd(), 'images')
        self.menues = MenuTree()

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

        for label, obj in items.items():
            limit = 30 // (len(group) + 1)
            group.append((label, self.colors.get(obj[1], "default")))
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

    def send_message(self, answer, menu, id_user, request):
        if answer:
            result = ""
            if answer[1]:
                path_file = os.path.join(self.images_dir, answer[1])
                if os.path.exists(path_file):
                    photo = self.vk_upload.photo_messages(path_file)
                    result = 'photo' + str(photo[0].get('owner_id')) + '_' + str(photo[0].get('id'))
            self.vk.method("messages.send",
                           {"peer_id": id_user,
                            "message": answer[0],
                            "keyboard": self.get_keyboard(menu.items) if menu.items else None,
                            "attachment": result,
                            "random_id": random.randint(1, 2147483647)})
        elif menu:
            self.vk.method("messages.send",
                           {"peer_id": id_user, "message": menu.get_menu(),
                            "keyboard": self.get_keyboard(menu.items),
                            "random_id": random.randint(1, 2147483647)})

    # обработка сообщения
    def handling_message(self, user_id: int, text_message: str):
        user_info = self.vk.method("users.get", values={"user_ids": user_id})
        user = User.create(user_id, user_info[0]['first_name'],
                           user_info[0]['last_name']).create_cache(self.menues.root.name).inc_request()
        answer, menu = self.controller.get_answer(text_message, user)
        self.send_message(answer, menu, user_id, text_message)

    # запуск цикла
    def run(self):
        while True:
            # try:
            # получаем сообщения
            messages = self.vk.method("messages.getConversations",
                                      {"offset": 0, "count": 20, "filter": "unanswered"})
            if messages["count"] >= 1:
                user_id = messages["items"][0]["last_message"]["from_id"]
                text_message = messages["items"][0]["last_message"]["text"]
                logging.info("From id: %d, message: %s" % (user_id, text_message))
                self.handling_message(user_id, text_message)
            # except Exception as E:
            #     logging.error(E)
            # time.sleep(1)
