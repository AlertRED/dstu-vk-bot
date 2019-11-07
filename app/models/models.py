import web_app.flask_app as flask_app
from datetime import datetime, date, time

db = flask_app.db
days_of_week = ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс')
days_of_week_enum = db.Enum(*days_of_week, name="days_of_week")
pairs_time = (time(8, 30), time(10, 15), time(12, 00), time(14, 15), time(16, 00), time(17, 45), time(19, 30))


def now_semester():
    month = datetime.now().month
    return 2 if (month >= 2 and not month >= 9) else 1


def now_week():
    a = date(datetime.now().year, 9, 1)
    offset = a.weekday() if a.weekday() < 6 else -1
    b = datetime.now().date()
    days = (b - a).days + offset
    return 1 if ((days // 7) % 2 == 0) else 2


from app.models.models_user import *
from app.models.models_faculty import *
from app.models.models_place import *
from app.models.models_other import *
from app.models.models_schedule import *

# Создание таблиц
db.Model.metadata.create_all(db.engine)
