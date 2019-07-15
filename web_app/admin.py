from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.models.models import *
from web_app import app

admin = Admin(app, name='DataBase')

admin.add_view(ModelView(User, db.session, name='Пользователи', category='Пользователи'))
admin.add_view(ModelView(UserCache, db.session, name='Кэш пользователей', category='Пользователи'))
admin.add_view(ModelView(UserAnswer, db.session, name='Ответы пользователей', category='Пользователи'))

admin.add_view(ModelView(Place, db.session, name='Места', category='Места'))
admin.add_view(ModelView(TypePlace, db.session, name='Тип места', category='Места'))
admin.add_view(ModelView(Schedule_place, db.session, name='Расписание', category='Места'))
admin.add_view(ModelView(Manager, db.session, name='Управляющий', category='Места'))
admin.add_view(ModelView(Post, db.session, name='Должность управляющего', category='Места'))
admin.add_view(ModelView(Phone_place, db.session, name='Телефон места', category='Места'))

admin.add_view(ModelView(Faculty, db.session, name='Факультеты', category='Структура университета'))
admin.add_view(ModelView(Dean, db.session, name='Деканы', category='Структура университета'))
admin.add_view(
    ModelView(Schedule_dean_office, db.session, name='Расписание деканата', category='Структура университета'))
admin.add_view(ModelView(Department, db.session, name='Кафедра', category='Структура университета'))
admin.add_view(
    ModelView(Manager_department, db.session, name='Управляющие кафедрами', category='Структура университета'))
admin.add_view(ModelView(Specialty, db.session, name='Специальности', category='Структура университета'))
admin.add_view(ModelView(Type_specialty, db.session, name='Типы специальностей', category='Структура университета'))

# if __name__ == '__main__':
#     app.debug = True
#     app.run()
