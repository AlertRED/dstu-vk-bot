from app.models.models_DB import Department, Faculty, Place

faculty = Faculty.get_faculty(name='Авиастроение')
Department.create('Авиастроение', abbreviation=None, cabinets=['402'], phones=['2589179', '2977566']). \
    add_manager('Флек', 'Михаил', 'Борисович').\
    add_faculty(faculty).\
    add_place(Place.get_place('Главный корпус'))

Department.create('Радиолокационные комплексы и навигационные системы', abbreviation='РКиНС', cabinets=None,
                  phones=['2435959']). \
    add_manager('Хохлов', 'Игорь', 'Евгеньевич').add_faculty(faculty). \
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Department.create('Теплоэнергетика и прикладная гидромеханика', abbreviation='ТиПГ', cabinets=['232а'], phones=['2589152']). \
    add_manager('Озерский', 'Анатолий', 'Иванович').add_faculty(faculty).add_place(Place.get_place('Корпус №10')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Department.create('Техническая эксплуатация летательных аппаратов и наземного оборудования', abbreviation='ТЭЛАиНО',
                  cabinets=['225'], phones=['2589157']). \
    add_manager('Решенкин', 'Андрей', 'Станиславович').add_faculty(faculty).add_place(Place.get_place('Корпус №10')).\
    add_schedule('пн', '8:30', '16:00'). \
    add_schedule('вт', '8:30', '16:00'). \
    add_schedule('ср', '8:30', '16:00'). \
    add_schedule('чт', '8:30', '16:00'). \
    add_schedule('пт', '8:30', '16:00')

Department.create('Технологии производства авиационных комплексов специального назначения', abbreviation='ТПАКСН',
                  cabinets=['403'], phones=['2589119']). \
    add_manager('Грудинин', 'Юрий', 'Владимирович').add_faculty(faculty).add_place(Place.get_place('Корпус №10')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

###

faculty = Faculty.get_faculty(abbreviation='АМиУ')
Department.create('Автоматизация производственных процессов', abbreviation='АПП', cabinets=['401', '404', '405', '407', '303'], phones=['2738510', '2738780']). \
    add_manager('Лукьянов', 'Александр', 'Дмитриевич').add_faculty(faculty).add_place(Place.get_place('Корпус №6')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Department.create('Гидравлика, гидропневмоавтоматика и тепловые процессы', abbreviation='ГГиТП', cabinets=['166', '194', '281'], phones=['2738326' , '2738594']). \
    add_manager('Грищенко', 'Вячеслав', 'Игоревич').add_faculty(faculty).add_place(Place.get_place('Главный корпус')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Department.create('Робототехника и мехатроника', abbreviation='РиМ', cabinets=['602'], phones=['2381359']). \
    add_manager('Лукьянов', 'Евгений', 'Анатольевич').add_faculty(faculty).add_place(Place.get_place('Корпус №6')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Department.create('Системы приводов', abbreviation='СП', cabinets=['701a'], phones=['2738465']). \
    add_manager('Харченко', 'Александр', 'Николаевич').add_faculty(faculty).add_place(Place.get_place('Корпус №2')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')


Department.create('Физика', abbreviation=None, cabinets=['433', '433а', '437', '437а'], phones=['2738516', '2738305']). \
    add_manager('Благин', 'Анатолий', 'Вячеславович').add_faculty(faculty).add_place(Place.get_place('Главный корпус')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')


Department.create('Электротехника и электроника', abbreviation='ЭиЭ', cabinets=['258', '260'], phones=['2738541', '2738301']). \
    add_manager('Лаврентьев', 'Анатолий', 'Александрович').add_faculty(faculty).add_place(Place.get_place('Главный корпус')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

###

faculty = Faculty.get_faculty(name='Агропромышленный')
Department.create('Инженерная и компьютерная графика', abbreviation='ИиКГ', cabinets=['327a', '340'], phones=['2738561', '2738520']). \
    add_manager('Чередниченко', 'Ольга', 'Павловна').add_faculty(faculty).add_place(Place.get_place('Главный корпус')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Department.create('Проектирование и технический сервис транспортно-технологических систем', abbreviation='ПиТСТТС', cabinets=['208', '209', '213'], phones=['2738347', '2738733']). \
    add_manager('Бутовченко', 'Андрей', 'Владимирович').add_faculty(faculty).add_place(Place.get_place('Главный корпус')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Department.create('Теоретическая и прикладная механика', abbreviation='ТиПМ', cabinets=['124', '125'], phones=['2381509', '2738320']). \
    add_manager('Соловьев', 'Аркадий', 'Николаевич').add_faculty(faculty).add_place(Place.get_place('Главный корпус')).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')
