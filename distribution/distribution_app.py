from time import sleep

from app.models.models import *

while True:
    (min_time,), users = User.get_users_with_min_remind_date()
    print(min_time)
    if users:
        print('Жду %s секунд' % min_time)
        sleep(min_time)
        for i, user in enumerate(users):
            print('Отправка сообщения №%d пользователю %s' % (i, user.first_name))
            user.inc_request()
    else:
        sleep(10)
