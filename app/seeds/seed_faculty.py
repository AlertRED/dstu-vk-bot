from app.models.models import Faculty, Department

Faculty.create('Авиастроение', None, 'a.227', 'a.228', None).add_dean('Зимонов', 'Олег', 'Владимирович'). \
    add_schedule('пн', '8:30', '7:00'). \
    add_schedule('вт', '8:30', '7:00'). \
    add_schedule('ср', '8:30', '7:00'). \
    add_schedule('чт', '8:30', '7:00'). \
    add_schedule('пт', '8:30', '7:00').add_departament(
    Department.create('Авиастроение', None, 'а.402', description=None, phone=['2589179'])).add_departament(
    Department.create('Радиолакационные комплексы и навигационные системы', 'РКиНС', 'а.402', description=None,
                      phone=['2435959'])).add_departament(
    Department.create('Теплоэнергетика и прикладная гидромеханика', 'ТиПГ', 'а.402', description=None,
                      phone=None)).add_departament(
    Department.create('Техническая эксплуатация летательных аппаратов и наземного оборудования', 'ТЭЛАиНО', 'а.402', description=None,
                      phone=None))
