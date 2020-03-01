from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from web_app.run import db, flask_app, models_DB

admin = Admin(flask_app, name='DataBase', url='/')

admin.add_view(ModelView(models_DB.User, db.session, name='Пользователи', category='Пользователи'))
admin.add_view(ModelView(models_DB.UserCache, db.session, name='Кэш пользователей', category='Пользователи'))
admin.add_view(ModelView(models_DB.UserAnswer, db.session, name='Ответы пользователей', category='Пользователи'))
admin.add_view(ModelView(models_DB.Review, db.session, name='Отзывы', category='Пользователи'))

admin.add_view(ModelView(models_DB.Place, db.session, name='Места', category='Места'))
admin.add_view(ModelView(models_DB.TypePlace, db.session, name='Тип места', category='Места'))
admin.add_view(ModelView(models_DB.SchedulePlace, db.session, name='Расписание', category='Места'))
admin.add_view(ModelView(models_DB.ManagerPlace, db.session, name='Управляющий', category='Места'))
admin.add_view(ModelView(models_DB.Post, db.session, name='Должность управляющего', category='Места'))

admin.add_view(ModelView(models_DB.Faculty, db.session, name='Факультеты', category='Структура университета'))
admin.add_view(ModelView(models_DB.Dean, db.session, name='Деканы', category='Структура университета'))
admin.add_view(
    ModelView(models_DB.ScheduleDeanOffice, db.session, name='Расписание деканата', category='Структура университета'))
admin.add_view(ModelView(models_DB.Department, db.session, name='Кафедра', category='Структура университета'))
admin.add_view(
    ModelView(models_DB.ManagerDepartment, db.session, name='Управляющие кафедрами', category='Структура университета'))
admin.add_view(ModelView(models_DB.Specialty, db.session, name='Специальности', category='Структура университета'))
admin.add_view(ModelView(models_DB.TypeSpecialty, db.session, name='Типы специальностей', category='Структура университета'))

admin.add_view(ModelView(models_DB.Teacher, db.session, name='Преподаватели', category='Расписание'))
admin.add_view(ModelView(models_DB.Group, db.session, name='Группы', category='Расписание'))
admin.add_view(ModelView(models_DB.Subject, db.session, name='Предметы', category='Расписание'))

admin.add_view(ModelView(models_DB.Log, db.session, name='Ошибки'))

