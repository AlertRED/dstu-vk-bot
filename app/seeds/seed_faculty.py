from sqlalchemy.orm import Session
from app.models.models import engine
from app.daos.faculty_dao import facultyDAO
from app.daos.place_dao import placeDAO

db = Session(bind=engine)
facultyDAO = facultyDAO(db)
placeDAO = placeDAO(db)

place = placeDAO.get_place_by_name('Корпус №10')
dean = facultyDAO.create_or_update_dean('Зимонов', 'Олег', 'Владимирович')
faculty_1 = facultyDAO.create_or_update_faculty('Авиастроение',
                                                None,place, '227', '228','',)

faculty_2 = facultyDAO.create_or_update_faculty('Информатика и вычислительная техника', 'ИиВТ', '347а', '',
                                                {'first_name': 'Зимонов', 'last_name': 'Олег',
                                                 'patronymic': 'Владимирович'})

faculty_3 = facultyDAO.create_or_update_faculty('Информатика и вычислительная техника', 'ИиВТ', '347а', '',
                                                {'first_name': 'Зимонов', 'last_name': 'Олег',
                                                 'patronymic': 'Владимирович'})

faculty_4 = facultyDAO.create_or_update_faculty('Информатика и вычислительная техника', 'ИиВТ', '347а', '',
                                                {'first_name': 'Зимонов', 'last_name': 'Олег',
                                                 'patronymic': 'Владимирович'})

faculty_5 = facultyDAO.create_or_update_faculty('Информатика и вычислительная техника', 'ИиВТ', '347а', '',
                                                {'first_name': 'Зимонов', 'last_name': 'Олег',
                                                 'patronymic': 'Владимирович'})

faculty_6 = facultyDAO.create_or_update_faculty('Информатика и вычислительная техника', 'ИиВТ', '347а', '',
                                                {'first_name': 'Зимонов', 'last_name': 'Олег',
                                                 'patronymic': 'Владимирович'})

faculty_7 = facultyDAO.create_or_update_faculty('Информатика и вычислительная техника', 'ИиВТ', '347а', '',
                                                {'first_name': 'Зимонов', 'last_name': 'Олег',
                                                 'patronymic': 'Владимирович'})

department = facultyDAO.create_or_update_department('Информационные технологии', 'ИТ', 'а.350', '', '273-83-41',
                                                    faculty, {'first_name': 'Борис', 'last_name': 'Соболь',
                                                              'patronymic': 'Владимирович'})

specialty = facultyDAO.create_or_update_specialty('Информационные системы и технологии', 'ИСиТ',
                                                  [{'code': '09.04.02', 'duration': 2, 'type': 'Магистратура'},
                                                   {'code': '09.03.02', 'duration': 4, 'type': 'Бакалавриат'}], faculty)
