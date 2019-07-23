from datetime import datetime

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
import web_app.__init__ as flask

db = flask.db

days_of_week = ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс')
days_of_week_enum = db.Enum(*days_of_week, name="days_of_week")


from app.models.faculty_models import *
from app.models.place_models import *
from app.models.user_models import *


# Создание таблицы
db.Model.metadata.create_all(db.engine)
