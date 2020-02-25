from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from web_app.run import db, flask_app, orm_models

admin = Admin(flask_app, name='DataBase', url='/')

admin.add_view(ModelView(orm_models.User, db.session, name='Пользователи', category='Пользователи'))
admin.add_view(ModelView(orm_models.UserCache, db.session, name='Кэш пользователей', category='Пользователи'))
admin.add_view(ModelView(orm_models.UserAnswer, db.session, name='Ответы пользователей', category='Пользователи'))
admin.add_view(ModelView(orm_models.Review, db.session, name='Отзывы', category='Пользователи'))

admin.add_view(ModelView(orm_models.Place, db.session, name='Места', category='Места'))
admin.add_view(ModelView(orm_models.TypePlace, db.session, name='Тип места', category='Места'))
admin.add_view(ModelView(orm_models.SchedulePlace, db.session, name='Расписание', category='Места'))
admin.add_view(ModelView(orm_models.ManagerPlace, db.session, name='Управляющий', category='Места'))
admin.add_view(ModelView(orm_models.Post, db.session, name='Должность управляющего', category='Места'))

admin.add_view(ModelView(orm_models.Faculty, db.session, name='Факультеты', category='Структура университета'))
admin.add_view(ModelView(orm_models.Dean, db.session, name='Деканы', category='Структура университета'))
admin.add_view(
    ModelView(orm_models.ScheduleDeanOffice, db.session, name='Расписание деканата', category='Структура университета'))
admin.add_view(ModelView(orm_models.Department, db.session, name='Кафедра', category='Структура университета'))
admin.add_view(
    ModelView(orm_models.ManagerDepartment, db.session, name='Управляющие кафедрами', category='Структура университета'))
admin.add_view(ModelView(orm_models.Specialty, db.session, name='Специальности', category='Структура университета'))
admin.add_view(ModelView(orm_models.TypeSpecialty, db.session, name='Типы специальностей', category='Структура университета'))

admin.add_view(ModelView(orm_models.Teacher, db.session, name='Преподаватели', category='Расписание'))
admin.add_view(ModelView(orm_models.Group, db.session, name='Группы', category='Расписание'))
admin.add_view(ModelView(orm_models.Subject, db.session, name='Предметы', category='Расписание'))

admin.add_view(ModelView(orm_models.Log, db.session, name='Ошибки'))

