from sqlalchemy.orm import Session
from app.models import Place, TypePlace, Day_of_week, Post, Phone_place, Manager, Schedule, engine


class placeDAO:

    def __init__(self, db: Session):
        self.db = db

    def _first_or_create_type_place(self, name):
        type_place = self.db.query(TypePlace).filter_by(name=name).first()
        if not type_place and name:
            type_place = TypePlace(name=name)
            self.db.add(type_place)
            self.db.commit()
        return type_place

    def _first_or_create_post(self, name):
        post = self.db.query(Post).filter_by(name=name).first()
        if not post and name:
            post = Post(name=name)
            self.db.add(post)
            self.db.commit()
        return post

    def _first_or_create_day_of_week(self, name):
        day = self.db.query(Day_of_week).filter_by(name=name).first()
        if not day and name:
            day = Day_of_week(name=name)
            self.db.add(day)
            self.db.commit()
        return day

    def _update_or_create_schedule(self, place, day_of_week, start_time=None, end_time=None,
                                   pause_start_time=None, pause_end_time=None):
        schedule = self.db.query(Schedule).filter_by(place=place, day_of_week=day_of_week).first()
        if not schedule and place and day_of_week:
            schedule = Schedule(start_time=start_time,
                                end_time=end_time,
                                pause_start_time=pause_start_time,
                                pause_end_time=pause_end_time,
                                place=place,
                                day_of_week=day_of_week)
            self.db.add(schedule)
        else:
            schedule.start_time = start_time
            schedule.end_time = end_time
            schedule.pause_start_time = pause_start_time
            schedule.pause_end_time = pause_end_time
            schedule.place = place
            schedule.day_of_week = day_of_week
        self.db.commit()
        return schedule

    def _first_or_create_phone_place(self, phone, place):
        phone_place = self.db.query(Phone_place).filter_by(place=place, phone=phone).first()
        if not phone_place and phone and place:
            phone_place = Phone_place(phone=phone, place=place)
            self.db.add(phone_place)
            self.db.commit()
        return phone_place

    def _update_or_create_manager(self, place, first_name, last_name, patronymic, post=None):
        manager = self.db.query(Manager).filter_by(place=place, first_name=first_name, last_name=last_name,
                                                   patronymic=patronymic).first()
        if not manager and first_name and last_name and patronymic:
            manager = Manager(first_name=first_name,
                              last_name=last_name,
                              patronymic=patronymic,
                              place=place,
                              post=post)
            self.db.add(manager)
        else:
            manager.post = post
        self.db.commit()
        return post

    def update_or_create_place(self, name, map_url=None, adress=None, type_place_name=None, schedules=None,
                               managers=None, phones=None):

        type_place = self._first_or_create_type_place(name=type_place_name) if type_place_name else None

        place = self.db.query(Place).filter_by(name=name).first()
        if not place:
            place = Place(name=name, map_url=map_url, adress=adress,
                          type_place=type_place)
            self.db.add(place)
        else:
            place.map_url = map_url
            place.adress = adress
            place.type_place = type_place
            place.name = name
        self.db.commit()

        if managers:
            for manager in managers:
                self._update_or_create_manager(place=place,
                                               first_name=manager["first_name"],
                                               last_name=manager["last_name"],
                                               patronymic=manager["patronymic"],
                                               post=self._first_or_create_post(manager["post"]))

        if phones:
            for phone in phones:
                self._first_or_create_phone_place(phone=phone, place=place)

        if schedules:
            for schedule in schedules:
                self._update_or_create_schedule(place,
                                                self._first_or_create_day_of_week(schedule["day_name"]),
                                                schedule["start_time"],
                                                schedule["end_time"],
                                                schedule["pause_start_time"],
                                                schedule["pause_end_time"])

        return place

    def get_place(self, name):
        place = self.db.query(Place).filter_by(name=name).first()
        return place


# if __name__ == '__main__':
db = Session(bind=engine)
placeDAO = placeDAO(db)
placeDAO.update_or_create_place('Главный корпус', map_url='ссылка на карту', adress='адрес места',
                                type_place_name='тип места', schedules=[
        {'day_name': 'пн', 'start_time': '12:00', 'end_time': '18:00', 'pause_start_time': '14:00',
         'pause_end_time': '15:00'},
        {'day_name': 'вт', 'start_time': '12:00', 'end_time': '18:00', 'pause_start_time': '14:00',
         'pause_end_time': '15:00'},
        {'day_name': 'ср', 'start_time': '12:00', 'end_time': '18:00', 'pause_start_time': '14:00',
         'pause_end_time': '15:00'},
        {'day_name': 'чт', 'start_time': '12:00', 'end_time': '18:00', 'pause_start_time': '14:00',
         'pause_end_time': '15:00'},
        {'day_name': 'пт', 'start_time': '12:00', 'end_time': '18:00', 'pause_start_time': '14:00',
         'pause_end_time': '15:00'},
        {'day_name': 'сб', 'start_time': '12:00', 'end_time': '16:00', 'pause_start_time': '14:00',
         'pause_end_time': '15:00'}],
                                managers=[{'first_name': 'Имя', 'last_name': 'Фамилия', 'patronymic': 'Отчество',
                                           'post': 'Должность'}],
                                phones=['+7-987-654-32-10', '+2-399-000'])
