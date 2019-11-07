from time import sleep

from app.models.models import *
from datetime import datetime

while True:
    (min_time,), users = User.get_users_remind()
    if users:
        delay = (min_time - datetime.now()).seconds
        print('Жду %s секунд' % delay)
        sleep(2)
        weekday = min_time.weekday()
        for i, user in enumerate(users):
            print(user.get_group().get_schedule(day=days_of_week[weekday], week=now_week(), semester=now_semester()))
            user.refresh_nearest_remind()
    else:
        print('Ничего не нашел, сплю 10 секунд')
        sleep(10)
