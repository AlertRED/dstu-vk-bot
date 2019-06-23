from sqlalchemy.orm import Session
from app.models.models import engine
from app.daos.faculty_dao import facultyDAO

db = Session(bind=engine)
facultyDAO = facultyDAO(db)

faculty = facultyDAO.create_or_update_faculty('Информатика и вычислительная техника', 'ИиВТ', '347а', '',
                                              {'first_name': 'Виталий', 'last_name': 'Поркшеян',
                                               'patronymic': 'Маркосович'})

department = facultyDAO.create_or_update_department('Информационные технологии', 'ИТ', 'а.350', '', '273-83-41',
                                                    faculty, {'first_name': 'Борис', 'last_name': 'Соболь',
                                                              'patronymic': 'Владимирович'})

specialty = facultyDAO.create_or_update_specialty('Информационные системы и технологии', 'ИСиТ',
                                                  [{'code': '09.04.02', 'duration': 2, 'type': 'Магистратура'},
                                                   {'code': '09.03.02', 'duration': 4, 'type': 'Бакалавриат'}], faculty)
