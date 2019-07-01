from sqlalchemy.orm import Session
from app.models.models import Place, TypePlace, Day_of_week, Post, Phone_place, Manager, Schedule_dean_office, Faculty, \
    Dean, \
    Department, Specialty, Type_specialty, Manager_department


class facultyDAO:

    def __init__(self, db: Session):
        self.db = db

    def create_or_update_dean(self, first_name: str, last_name: str, patronymic: str, faculty: Faculty):
        dean = self.db.query(Dean).filter_by(faculty=faculty).first()
        if dean:
            dean.first_name = first_name
            dean.last_name = last_name
            dean.patronymic = patronymic
        else:
            dean = Dean(first_name=first_name, last_name=last_name, patronymic=patronymic, faculty=faculty)
            self.db.add(dean)
        self.db.commit()

    def create_or_update_manager(self, first_name: str, last_name: str, patronymic: str, department: Department):
        maneger = self.db.query(Manager_department).filter_by(department=department).first()
        if maneger:
            maneger.first_name = first_name
            maneger.last_name = last_name
            maneger.patronymic = patronymic
        else:
            maneger = Manager_department(first_name=first_name, last_name=last_name, patronymic=patronymic,
                                         department=department)
            self.db.add(maneger)
        self.db.commit()

    def create_or_update_type_specialty(self, code: str, duration: int, type: str, specialty: Specialty):
        type_specialty = self.db.query(Type_specialty).filter_by(specialty=specialty, type=type).first()
        if type_specialty:
            type_specialty.code = code
            type_specialty.duration = duration
        else:
            type_specialty = Type_specialty(duration=duration, code=code, type=type, specialty=specialty)
            self.db.add(type_specialty)
        self.db.commit()

    def create_or_update_faculty(self, name: str, abbreviation: str, place: Place, cabinet_dean: str,
                                 cabinet_dean_office: str, phone: str, dean: dict):
        faculty = self.db.query(Faculty).filter_by(name=name).first()

        if faculty:
            faculty.abbreviation = abbreviation
            faculty.cabinet_dean = cabinet_dean
            faculty.cabinet_dean_office = cabinet_dean_office
            faculty.phone = phone
            faculty.place = place
        else:
            faculty = Faculty(name=name, abbreviation=abbreviation, cabinet_dean_office=cabinet_dean_office,
                              cabinet_dean=cabinet_dean, phone=phone, place=place)
            self.db.add(faculty)
        self.db.commit()

        self.create_or_update_dean(first_name=dean['first_name'], last_name=dean['last_name'],
                                   patronymic=dean['patronymic'], faculty=faculty)
        return faculty

    def create_or_update_department(self, name: str, abbreviation: str, cabinet: str, description: str, phone: str,
                                    faculty: Faculty, manager: dict):
        department = self.db.query(Department).filter_by(name=name).first()
        if department:
            department.abbreviation = abbreviation
            department.cabinet = cabinet
            department.description = description
            department.phone = phone
            department.faculty = faculty
        else:
            department = Department(name=name, abbreviation=abbreviation, cabinet=cabinet, description=description,
                                    phone=phone, faculty=faculty)
            self.db.add(department)
        self.db.commit()
        self.create_or_update_manager(first_name=manager['first_name'], last_name=manager['last_name'],
                                      patronymic=manager['patronymic'], department=department)
        return department

    def create_or_update_specialty(self, name: str, abbreviation: str, types_specialty: list, faculty: Faculty):

        specialty = self.db.query(Specialty).filter_by(name=name).first()
        if specialty:
            specialty.name = name
            specialty.abbreviation = abbreviation
            specialty.faculty = faculty
        else:
            specialty = Specialty(name=name, abbreviation=abbreviation, faculty=faculty)
            self.db.add(specialty)
        self.db.commit()

        for i in types_specialty:
            self.create_or_update_type_specialty(i.get('code'), i.get('duration'), i.get('type'), specialty)

        return specialty
