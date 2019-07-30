
import web_app.flask_app as flask_app
db = flask_app.db

days_of_week = ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс')
days_of_week_enum = db.Enum(*days_of_week, name="days_of_week")

from app.models.user_models import *
from app.models.faculty_models import *
from app.models.place_models import *
from app.models.other_models import *

# Создание таблиц
db.Model.metadata.create_all(db.engine)
