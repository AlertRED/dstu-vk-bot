from time import sleep

from vk_api import vk_api

from app.models.models_DB import *
from datetime import datetime


class NotifyApp:
    __timeout = 60

    def __init__(self):
        vk = vk_api.VkApi(token=Config.VK_TOKEN)
        print('[*] Авторизация с ВКонтакте... ', end='')
        vk._auth_token()
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
        return True

    @staticmethod
    def __send_notify(users, time: datetime):
        for i, user in enumerate(users):
            weekday = time.weekday()
            # print(user.get_group().get_schedule(day=days_of_week[weekday], week=current_week(),
            #                                     semester=1)) #now_semester()
            print(user)
            print(user.group.name)
            print(user.remind_date)
            print(days_of_week[weekday])
            user.refresh_nearest_remind()

    # Отправляет сообщения ближайшим по времени пользователям с их расписанием и обновляет их время
    @staticmethod
    def run():
        while True:
            time, users = NotifyApp.__get_near_time_users()
            delay_seconds = int((time - datetime.now()).total_seconds())

            while delay_seconds > 2:
                if NotifyApp.__is_changed_db():
                    time, users = NotifyApp.__get_near_time_users()
                delay_seconds = int((time - datetime.now()).total_seconds())
            else:
                if not users:
                    continue

            NotifyApp.__send_notify(users, time)


if __name__ == '__main__':
    NotifyApp.run()