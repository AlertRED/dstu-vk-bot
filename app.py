from sqlalchemy.orm import Session
from scratch import Treatment
from user_dao import userDAO
import vk_api
import time
import random



class app:
    def __init__(self, db: Session):
        self.db = db
        self.userDAO = userDAO(self.db)
        self.treatment = Treatment(self.userDAO)

        self.token = "1fe7ce1542f80ded456d1c65dc8daca77aa29e539977159f1a9501bf2bd789f960c4497fea25713e6bd57"

        self.vk = vk_api.VkApi(token=self.token)
        self.vk._auth_token()

    def run(self):
        # id_user = input("Введите id пользователя: ")

        while True:
            try:
                messages = self.vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
                if messages["count"] >= 1:
                    id = messages["items"][0]["last_message"]["from_id"]
                    body = messages["items"][0]["last_message"]["text"]
                    vk_user = self.vk.method("users.get", values={"user_ids": id})
                    print(body)
                    print(vk_user)
                    ##
                    user = self.userDAO.first_or_create_user(id)
                    # command = input("Введите команду: ")
                    answer, menu = self.new_message(user, body)
                    if answer:
                        self.vk.method("messages.send",
                                  {"peer_id": id, "message": answer, "random_id": random.randint(1, 2147483647)})
                    if menu:
                        self.vk.method("messages.send",
                                  {"peer_id": id, "message": menu, "random_id": random.randint(1, 2147483647)})
            except Exception as E:
                    print(E)
                    time.sleep(1)


    def new_message(self, user, command):
        answer, menu = self.treatment.get_answer(command, user)
        return answer, menu.get_menu()


