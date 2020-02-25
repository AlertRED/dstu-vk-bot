from app.models.orm_models import *

# специальность
class TypeSpecialty(Base):
    __tablename__ = 'type_specialty'
    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String, nullable=False)
    type = db.Column(db.Enum('Бакалавриат', 'Магистратура', 'Аспирантура', name="type_specialty_enum"), nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    specialty_id = db.Column(db.Integer, db.ForeignKey('specialty.id'))
    specialty = relationship("Specialty", back_populates="types")

    def __repr__(self):
        return self.code

    @staticmethod
    def get_type_specialty(code):
        return session.query(TypeSpecialty).filter_by(code=code).first()

    @staticmethod
    def create(code, type, duration):
        type_specialty = TypeSpecialty.get_type_specialty(code)
        if not type_specialty:
            type_specialty = TypeSpecialty(code=code, type=type, duration=duration)
            session.add(type_specialty)
            session.commit()
        return type_specialty


class Specialty(Base):
    __tablename__ = 'specialty'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    abbreviation = db.Column(db.String, nullable=False)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="specialties")
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = relationship("Department", uselist=False, back_populates="specialties")
    types = relationship("TypeSpecialty", back_populates="specialty")

    def __repr__(self):
        return self.name

    @staticmethod
    def get_specialty(name):
        return session.query(Specialty).filter_by(name=name).first()

    @staticmethod
    def create(name, abbreviation):
        specialty = Specialty.get_specialty(name)
        if not specialty:
            specialty = Specialty(name=name, abbreviation=abbreviation)
            session.add(specialty)
            session.commit()
        return specialty

    def add_type(self, code, type, duration):
        type_specialty = TypeSpecialty.get_type_specialty(code)
        if not type_specialty:
            self.types.append(TypeSpecialty.create(code, type, duration))
        return self


# кафедра

class ManagerDepartment(Base):
    __tablename__ = 'manager_department'
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    patronymic = db.Column(db.String, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = relationship("Department", uselist=False, back_populates="manager")

    def __repr__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.patronymic)

    @staticmethod
    def get_manager(first_name, last_name, patronymic):
        return session.query(ManagerDepartment).filter_by(first_name=first_name, last_name=last_name,
                                                             patronymic=patronymic).first()

    @staticmethod
    def create(first_name, last_name, patronymic):
        manager = ManagerDepartment.get_manager(first_name, last_name, patronymic)
        if not manager:
            manager = ManagerDepartment(first_name=first_name, last_name=last_name, patronymic=patronymic)
            session.add(manager)
            session.commit()
        return manager


class ScheduleDepartment(Base):
    __tablename__ = 'schedule_department'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    pause_start_time = db.Column(db.Time)
    pause_end_time = db.Column(db.Time)
    day_of_week = db.Column(days_of_week_enum)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = relationship("Department", back_populates="schedules")

    def __repr__(self):
        return '%s. %s - %s (%s - %s)' % (
            self.day_of_week, self.start_time, self.end_time, self.pause_start_time, self.pause_end_time)

    def add_day_of_week(self, name):
        self.day_of_week = name
        session.commit()
        return self

    @staticmethod
    def get_schedule(department, day_name):
        return session.query(ScheduleDepartment).filter_by(department=department,
                                                              day_of_week=day_name).first()

    @staticmethod
    def create(start_time, end_time, pause_start_time, pause_end_time):
        schedule = ScheduleDepartment(start_time=start_time, end_time=end_time, pause_start_time=pause_start_time,
                                      pause_end_time=pause_end_time)
        session.add(schedule)
        session.commit()
        return schedule


class Department(Base):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    abbreviation = db.Column(db.String)
    description = db.Column(db.String)
    phones = db.Column(ARRAY(db.String), server_default="{}")
    cabinets = db.Column(ARRAY(db.String), server_default="{}")

    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    place = relationship('Place', back_populates="departments")

    schedules = relationship("ScheduleDepartment", back_populates="department")
    specialties = relationship("Specialty", back_populates="department")

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="departments")

    manager = relationship("ManagerDepartment", uselist=False, back_populates="department")

    def __repr__(self):
        return self.name

    @staticmethod
    def get_department(name=None, abbreviation=None):
        if name:
            return session.query(Department).filter_by(name=name).first()
        return session.query(Department).filter_by(abbreviation=abbreviation).first()

    @staticmethod
    def all(faculty=None):
        if faculty:
            return session.query(Department).filter_by(faculty=faculty).all()
        return session.query(Department).filter_by().all()

    @staticmethod
    def create(name, abbreviation=None, cabinets=None, description=None, phones=None):
        department = Department.get_department(name)
        if not department:
            department = Department(name=name, abbreviation=abbreviation, cabinets=cabinets, description=description,
                                    phones=phones)
            session.add(department)
            session.commit()
        return department

    def add_manager(self, first_name, last_name, patronymic):
        self.manager = ManagerDepartment.create(first_name, last_name, patronymic)
        session.commit()
        return self

    def add_faculty(self, faculty):
        self.faculty = faculty
        session.commit()
        return self

    def add_place(self, place):
        self.place = place
        session.commit()
        return self

    def add_schedule(self, day_name, start_time, end_time, pause_start_time=None, pause_end_time=None):
        schedule = ScheduleDepartment.get_schedule(self, day_name)
        if not schedule:
            self.schedules.append(
                ScheduleDepartment.create(start_time, end_time, pause_start_time, pause_end_time).add_day_of_week(
                    day_name))
        return self


# факультет
class ScheduleDeanOffice(Base):
    __tablename__ = 'schedule_dean_office'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    pause_start_time = db.Column(db.Time)
    pause_end_time = db.Column(db.Time)

    day_of_week = db.Column(days_of_week_enum)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="schedules")

    def __repr__(self):
        return '%s. %s - %s (%s - %s)' % (
            self.day_of_week, self.start_time, self.end_time, self.pause_start_time, self.pause_end_time)

    def add_day_of_week(self, name):
        self.day_of_week = name
        session.commit()
        return self

    @staticmethod
    def get_schedule(faculty, day_name):
        return session.query(ScheduleDeanOffice).filter_by(faculty=faculty,
                                                              day_of_week=day_name).first()

    @staticmethod
    def create(start_time, end_time, pause_start_time, pause_end_time):
        schedule = ScheduleDeanOffice(start_time=start_time, end_time=end_time, pause_start_time=pause_start_time,
                                      pause_end_time=pause_end_time)
        session.add(schedule)
        session.commit()
        return schedule


class Dean(Base):
    __tablename__ = 'dean'
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    patronymic = db.Column(db.String, nullable=False)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="dean")

    def __repr__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.patronymic)

    @staticmethod
    def get_dean(first_name, last_name, patronymic):
        return session.query(Dean).filter_by(first_name=first_name, last_name=last_name,
                                                patronymic=patronymic).first()

    @staticmethod
    def create(first_name, last_name, patronymic):
        dean = Dean.get_dean(first_name, last_name, patronymic)
        if not dean:
            dean = Dean(first_name=first_name, last_name=last_name, patronymic=patronymic)
            session.add(dean)
            session.commit()
        return dean


class Faculty(Base):
    __tablename__ = 'faculty'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    abbreviation = db.Column(db.String)
    cabinet_dean = db.Column(ARRAY(db.String), server_default="{}")
    cabinet_dean_office = db.Column(ARRAY(db.String), server_default="{}")

    phones = db.Column(ARRAY(db.String), server_default="{}")

    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    place = relationship('Place', back_populates="faculties")

    schedules = relationship("ScheduleDeanOffice", back_populates="faculty")
    dean = relationship("Dean", uselist=False, back_populates="faculty")
    departments = relationship("Department", back_populates="faculty")
    specialties = relationship("Specialty", back_populates="faculty")

    def __repr__(self):
        return self.name

    @staticmethod
    def all():
        return session.query(Faculty).all()

    @staticmethod
    def get_faculty(name=None, abbreviation=None):
        if name:
            return session.query(Faculty).filter_by(name=name).first()
        elif abbreviation:
            return session.query(Faculty).filter_by(abbreviation=abbreviation).first()

    @staticmethod
    def create(name, abbreviation, cabinet_dean, cabinet_dean_office, phones):
        faculty = Faculty.get_faculty(name)
        if not faculty:
            faculty = Faculty(name=name, abbreviation=abbreviation, cabinet_dean=cabinet_dean,
                              cabinet_dean_office=cabinet_dean_office, phones=phones)
            session.add(faculty)
            session.commit()
        return faculty

    def add_dean(self, last_name, first_name, patronymic):
        self.dean = Dean.create(first_name, last_name, patronymic)
        session.commit()
        return self

    def add_schedule(self, day_name, start_time, end_time, pause_start_time=None, pause_end_time=None):
        schedule = ScheduleDeanOffice.get_schedule(self, day_name)
        if not schedule:
            self.schedules.append(
                ScheduleDeanOffice.create(start_time, end_time, pause_start_time, pause_end_time).add_day_of_week(
                    day_name))
        return self

    def add_departament(self, departament: Department):
        if departament not in self.departments:
            self.departments.append(departament)
        return self

    def add_specialty(self, specialty: Specialty):
        if specialty not in self.specialties:
            self.specialties.append(specialty)
        return self
