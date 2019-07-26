from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models.models import *
from web_app import flask_app

admin = Admin(flask_app, name='DataBase', url='/')

admin.add_view(ModelView(User, db.session, name='Пользователи', category='Пользователи'))
admin.add_view(ModelView(UserCache, db.session, name='Кэш пользователей', category='Пользователи'))
admin.add_view(ModelView(UserAnswer, db.session, name='Ответы пользователей', category='Пользователи'))
admin.add_view(ModelView(Review, db.session, name='Отзывы', category='Пользователи'))

admin.add_view(ModelView(Place, db.session, name='Места', category='Места'))
admin.add_view(ModelView(TypePlace, db.session, name='Тип места', category='Места'))
admin.add_view(ModelView(SchedulePlace, db.session, name='Расписание', category='Места'))
admin.add_view(ModelView(ManagerPlace, db.session, name='Управляющий', category='Места'))
admin.add_view(ModelView(Post, db.session, name='Должность управляющего', category='Места'))

admin.add_view(ModelView(Faculty, db.session, name='Факультеты', category='Структура университета'))
admin.add_view(ModelView(Dean, db.session, name='Деканы', category='Структура университета'))
admin.add_view(
    ModelView(ScheduleDeanOffice, db.session, name='Расписание деканата', category='Структура университета'))
admin.add_view(ModelView(Department, db.session, name='Кафедра', category='Структура университета'))
admin.add_view(
    ModelView(ManagerDepartment, db.session, name='Управляющие кафедрами', category='Структура университета'))
admin.add_view(ModelView(Specialty, db.session, name='Специальности', category='Структура университета'))
admin.add_view(ModelView(TypeSpecialty, db.session, name='Типы специальностей', category='Структура университета'))
