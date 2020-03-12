import random
from time import sleep

from vk_api import vk_api

from app.models.models_DB import *
from datetime import datetime


class NotifyApp:
    __timeout = 60

    def __init__(self):
        self.vk = vk_api.VkApi(token=Config.VK_TOKEN)
        print('[*] Авторизация с ВКонтакте... ', end='')
        self.vk._auth_token()
        print('Успешно')

    # Возвращает ближайших по времени пользователей для отправки им расписания
    @staticmethod
    def __get_near_time_users():
        while True:
            (min_time,), users = User.get_users_remind()
            if not min_time:
                sleep(NotifyApp.__timeout)
                continue
            if min_time > datetime.now():
                break
            else:
                for user in users:
                    user.refresh_nearest_remind()
        return min_time, users

    @staticmethod
    def __is_changed_db():
        param = Meta.get_first('change_db_notify')
        return param and param.get_and_change_boolean(new_status=False)

    def __send_notify(self, users, time: datetime):
        for i, user in enumerate(users):
            user.refresh_nearest_remind()
            schedule = user.get_group().get_schedule(day=days_of_week[time.weekday()-4], week=2, semester=1)
            message = '\n'.join('-%i: %s (%s)' % (item.number, item.name, item.cabinet if not None else 'ауд. -') for item in schedule)
            self.vk.method("messages.send",
                           {"peer_id": user.vk_id,
                            "message": message,
                            "random_id": random.randint(1, 2147483647)})

    # Отправляет сообщения ближайшим по времени пользователям с их расписанием и обновляет их время
    def run(self):
        while True:
            time, users = NotifyApp.__get_near_time_users()
            # time = datetime.now() + timedelta(seconds=1)
            delay_seconds = int((time - datetime.now()).total_seconds())
            while delay_seconds > 0:
                sleep(1)
                if NotifyApp.__is_changed_db():
                    time, users = NotifyApp.__get_near_time_users()
                delay_seconds = int((time - datetime.now()).total_seconds())
            if users:
                self.__send_notify(users, time)


if __name__ == '__main__':
   notify = NotifyApp()
   notify.run()