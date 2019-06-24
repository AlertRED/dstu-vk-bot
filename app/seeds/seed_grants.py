from sqlalchemy.orm import Session
from app.models.models import engine
from app.daos.grants_dao import grantDAO

db = Session(bind=engine)
grantDAO = grantDAO(db)

grantDAO.create_or_update_grant('Гос. академическая стипендия', False,
                                ['отсутствие по итогам сессии оценки ниже 4',
                                 'отсутствие по итогам сессии задолженности',
                                 'исключение, если является иностранным гражданином'],
                                [{'foreigner': True, 'conditions': 'иностранным гражданам',
                                  'form_of_study': 'Бакалавриат', 'money': 1700},
                                 {'foreigner': True, 'conditions': 'сессия закрыта на "хорошо"',
                                  'form_of_study': 'Бакалавриат', 'money': 2700},
                                 {'foreigner': True, 'conditions': 'сессия закрыта на "хорошо" и "отлично"',
                                  'form_of_study': 'Бакалавриат', 'money': 3100},
                                 {'foreigner': True, 'conditions': 'сессия закрыта на и "отлично"',
                                  'form_of_study': 'Бакалавриат', 'money': 3500}])
