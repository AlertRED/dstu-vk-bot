from time import sleep

from vk_api import VkApi

from app.models.orm_models import *
from datetime import datetime


class DistributionApp:
    __timeout = 60

    def __init__(self, vk: VkApi):
        self.vk = vk

    # Возвращает ближайших по времени пользователей для отправки им расписания
    @staticmethod
    def get_near_time_users():
        while True:
            (min_time,), users = User.get_users_remind()
            if not min_time:
                sleep(DistributionApp.__timeout)
                continue
            if min_time > datetime.now():
                break
            else:
                for user in users:
                    user.refresh_nearest_remind()
        return min_time, users

    # Осправляет сообщения ближайшим по времени пользователям с их расписанием и обновляет их время
    @staticmethod
    def run():
        while True:
            min_time, users = DistributionApp.get_near_time_users()
            if users:
                delay_seconds = int((min_time - datetime.now()).total_seconds())
                weekday = min_time.weekday()
                for i, user in enumerate(users):
                    print(user.get_group().get_schedule(day=days_of_week[weekday], week=current_week(),
                                                        semester=1)) #now_semester()
                    print(user)
                    user.refresh_nearest_remind()
                break


if __name__ == '__main__':
    DistributionApp.run()