from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from web_app.run import flask_app, models_DB

admin = Admin(flask_app, name='DataBase', url='/')

admin.add_view(ModelView(models_DB.User, models_DB.session, name='Пользователи', category='Пользователи'))
admin.add_view(ModelView(models_DB.UserCache, models_DB.session, name='Кэш пользователей', category='Пользователи'))
admin.add_view(ModelView(models_DB.UserAnswer, models_DB.session, name='Ответы пользователей', category='Пользователи'))
admin.add_view(ModelView(models_DB.DinamicItems, models_DB.session, name='Динамические пункты', category='Пользователи'))
admin.add_view(ModelView(models_DB.Review, models_DB.session, name='Отзывы', category='Пользователи'))

admin.add_view(ModelView(models_DB.Place, models_DB.session, name='Места', category='Места'))
admin.add_view(ModelView(models_DB.TypePlace, models_DB.session, name='Тип места', category='Места'))
admin.add_view(ModelView(models_DB.SchedulePlace, models_DB.session, name='Расписание', category='Места'))
admin.add_view(ModelView(models_DB.ManagerPlace, models_DB.session, name='Управляющий', category='Места'))
admin.add_view(ModelView(models_DB.Post, models_DB.session, name='Должность управляющего', category='Места'))

admin.add_view(ModelView(models_DB.Faculty, models_DB.session, name='Факультеты', category='Структура университета'))
admin.add_view(ModelView(models_DB.Dean, models_DB.session, name='Деканы', category='Структура университета'))
admin.add_view(
    ModelView(models_DB.ScheduleDeanOffice, models_DB.session, name='Расписание деканата', category='Структура университета'))
admin.add_view(ModelView(models_DB.Department, models_DB.session, name='Кафедра', category='Структура университета'))
admin.add_view(
    ModelView(models_DB.ManagerDepartment, models_DB.session, name='Управляющие кафедрами', category='Структура университета'))
admin.add_view(ModelView(models_DB.Specialty, models_DB.session, name='Специальности', category='Структура университета'))
admin.add_view(ModelView(models_DB.TypeSpecialty, models_DB.session, name='Типы специальностей', category='Структура университета'))

admin.add_view(ModelView(models_DB.Teacher, models_DB.session, name='Преподаватели', category='Расписание'))
admin.add_view(ModelView(models_DB.Group, models_DB.session, name='Группы', category='Расписание'))
admin.add_view(ModelView(models_DB.Subject, models_DB.session, name='Предметы', category='Расписание'))

admin.add_view(ModelView(models_DB.Log, models_DB.session, name='Ошибки'))
admin.add_view(ModelView(models_DB.Meta, models_DB.session, name='Meta'))

