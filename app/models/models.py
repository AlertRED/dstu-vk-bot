
import web_app.flask_app as flask_app
db = flask_app.db

days_of_week = ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс')
days_of_week_enum = db.Enum(*days_of_week, name="days_of_week")

from app.models.models_user import *
from app.models.models_faculty import *
from app.models.models_place import *
from app.models.models_other import *
from app.models.models_schedule import *

# Создание таблиц
db.Model.metadata.create_all(db.engine)
