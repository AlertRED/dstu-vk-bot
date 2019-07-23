from app.models.models import Department, Faculty, Place

faculty = Faculty.get_faculty(name='Авиастроение')
Department.create('Авиастроение', abbreviation=None, cabinet=['402'], phone=['2589179']). \
    add_manager('Флек', 'Михаил', 'Борисович').add_faculty(faculty).add_place(Place.get_place('Главный корпус'))

Department.create('Радиолокационные комплексы и навигационные системы', abbreviation='РКиНС', cabinet=None,
                  phone=['2435959']). \
    add_manager('Хохлов', 'Игорь', 'Евгеньевич').add_faculty(faculty). \
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Department.create('Теплоэнергетика и прикладная гидромеханика', abbreviation='ТиПГ', cabinet=['232а'], phone=['2589152']). \
    add_manager('Озерский', 'Анатолий', 'Иванович').add_faculty(faculty).add_place(Place.get_place('Корпус №10')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Department.create('Техническая эксплуатация летательных аппаратов и наземного оборудования', abbreviation='ТЭЛАиНО',
                  cabinet=['225'], phone=['2589157']). \
    add_manager('Решенкин', 'Андрей', 'Станиславович').add_faculty(faculty).add_place(Place.get_place('Корпус №10')).\
    add_schedule('пн', '8:30', '16:00'). \
    add_schedule('вт', '8:30', '16:00'). \
    add_schedule('ср', '8:30', '16:00'). \
    add_schedule('чт', '8:30', '16:00'). \
    add_schedule('пт', '8:30', '16:00')

Department.create('Технологии производства авиационных комплексов специального назначения', abbreviation='ТПАКСН',
                  cabinet=['403'], phone=['2589119']). \
    add_manager('Грудинин', 'Юрий', 'Владимирович').add_faculty(faculty).add_place(Place.get_place('Корпус №10')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

###

faculty = Faculty.get_faculty(abbreviation='АМиУ')
Department.create('Автоматизация производственных процессов', abbreviation='АПП', cabinet=['401','404','405','407','303'], phone=['2738510', '2738780']). \
    add_manager('Лукьянов', 'Александр', 'Дмитриевич').add_faculty(faculty).add_place(Place.get_place('Корпус №6')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Department.create('Гидравлика, гидропневмоавтоматика и тепловые процессы', abbreviation='ГГиТП', cabinet=['166', '194', '281'], phone=['2738326' , '2738594']). \
    add_manager('Грищенко', 'Вячеслав', 'Игоревич').add_faculty(faculty).add_place(Place.get_place('Главный корпус')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Department.create('Робототехника и мехатроника', abbreviation='РиМ', cabinet=['602'], phone=['2381359']). \
    add_manager('Лукьянов', 'Евгений', 'Анатольевич').add_faculty(faculty).add_place(Place.get_place('Корпус №6')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Department.create('Системы приводов', abbreviation='СП', cabinet=['701a'], phone=['2738465']). \
    add_manager('Харченко', 'Александр', 'Николаевич').add_faculty(faculty).add_place(Place.get_place('Корпус №2')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')


Department.create('Физика', abbreviation=None, cabinet=['433', '433а','437','437а'], phone=['2738516', '2738305']). \
    add_manager('Благин', 'Анатолий', 'Вячеславович').add_faculty(faculty).add_place(Place.get_place('Глаыный корпус')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')


Department.create('Электротехника и электроника', abbreviation='ЭиЭ', cabinet=['258', '260'], phone=['2738541', '2738301']). \
    add_manager('Лаврентьев', 'Анатолий', 'Александрович').add_faculty(faculty).add_place(Place.get_place('Глаыный корпус')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

###

faculty = Faculty.get_faculty(abbreviation='АМиУ')
Department.create('Автоматизация производственных процессов', abbreviation='АПП', cabinet=['401','404','405','407','303'], phone=['2738510', '2738780']). \
    add_manager('Лукьянов', 'Александр', 'Дмитриевич').add_faculty(faculty).add_place(Place.get_place('Корпус №6')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')
