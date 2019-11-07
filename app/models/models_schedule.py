from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.models import db, days_of_week_enum


# Группа
class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    original_name = db.Column(db.String)
    year = db.Column(db.String)
    number_by_site = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, onupdate=datetime.utcnow)

    subjects = relationship("Subject", back_populates="group")

    def __repr__(self):
        return self.name

    @staticmethod
    def get_group(name):
        return db.session.query(Group).filter_by(name=name).first()

    @staticmethod
    def create(name, year, number_by_site, semester):
        group = Group.get_group(name)
        if not group:
            group = Group(name=name, year=year, number_by_site=number_by_site, semester=semester)
            db.session.add(group)
            db.session.commit()
        return group

    def add_subject(self, subject):
        self.subjects.append(subject)
        db.session.commit()
        return self

    def get_schedule(self, day=None, week=None, semester=None, number=None) -> list:
        return [subject for subject in self.subjects if
                ((week is None) or subject.week == week) and
                ((semester is None) or subject.semester == semester) and
                ((day is None) or subject.day_of_week == day) and
                ((number is None) or subject.number == number)][::-1]


# Преподаватель
class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    patronymic = db.Column(db.String)

    subjects = relationship("Subject", back_populates="teacher")

    def __repr__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.patronymic)

    @staticmethod
    def get_teacher(first_name, last_name, patronymic):
        return db.session.query(Teacher).filter_by(first_name=first_name, last_name=last_name,
                                                   patronymic=patronymic).first()

    @staticmethod
    def create(first_name, last_name, patronymic):
        teacher = Teacher.get_teacher(first_name, last_name, patronymic)
        if not teacher:
            teacher = Teacher(first_name=first_name, last_name=last_name, patronymic=patronymic)
            db.session.add(teacher)
            db.session.commit()
        return teacher


# Предмет в расписании
class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    number = db.Column(db.Integer)  # номер пары
    week = db.Column(db.Integer)  # номер недели
    semester = db.Column(db.Integer)
    cabinet = db.Column(db.String)

    day_of_week = db.Column(days_of_week_enum)

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    group = relationship("Group", back_populates="subjects")
    teacher = relationship("Teacher", back_populates="subjects")

    def __repr__(self):
        return '%s: %s' % (self.day_of_week, self.name)

    @staticmethod
    def get_subject(name, number, week, semester, day_of_week):
        return db.session.query(Subject).filter_by(name=name, number=number, week=week, semester=semester,
                                                   day_of_week=day_of_week).first()

    @staticmethod
    def create(name, number, week, semester, day_of_week):
        subject = Subject.get_subject(name, number, week, semester, day_of_week)
        if not subject:
            subject = Subject(name=name, number=number, week=week, semester=semester, day_of_week=day_of_week)
            db.session.add(subject)
            db.session.commit()
        return subject

    def set_teacher(self, first_name, last_name, patronymic):
        teacher = Teacher.create(first_name=first_name, last_name=last_name, patronymic=patronymic)
        self.teacher = teacher
        db.session.commit()
        return self
