from app.models.models_menu import Menu
from app.daos.place_dao import placeDAO
from app.daos.grants_dao import grantDAO


class MenuTree:

    def __init__(self, placeDAO: placeDAO, grantDAO: grantDAO):

        self.placeDAO = placeDAO
        self.grantDAO = grantDAO
        self.root = Menu("Главное меню")

        # ДГТУ и АСА

        self.places_menu = Menu('Места и объекты')
        self.dstu_menu = Menu('ДГТУ')
        self.asa_menu = Menu('АСА')

        self.dstu_housings_menu = self.get_place_menu('Корпуса', 'Корпус')
        self.dstu_cafe_menu = self.get_place_menu('Кафе', 'Кафе')
        self.dstu_hostels_menu = self.get_place_menu('Общежития', 'Общежитие')
        self.dstu_sport_menu = self.get_place_menu('Спортивные комплексы', 'Спортивные комплексы')
        self.dstu_other_places_menu = self.get_place_menu('Другое', 'Другое')

        self.dstu_menu.add_menu_item(self.dstu_housings_menu.name, self.dstu_housings_menu)
        self.dstu_menu.add_menu_item(self.dstu_cafe_menu.name, self.dstu_cafe_menu)
        self.dstu_menu.add_menu_item(self.dstu_hostels_menu.name, self.dstu_hostels_menu)
        self.dstu_menu.add_menu_item(self.dstu_sport_menu.name, self.dstu_sport_menu)
        self.dstu_menu.add_menu_item(self.dstu_other_places_menu.name, self.dstu_other_places_menu)

        self.places_menu.add_menu_item('ДГТУ', self.dstu_menu)

        self.asa_housings_menu = self.get_place_menu('Корпуса', 'Корпус')
        self.asa_cafe_menu = self.get_place_menu('Кафе', 'Кафе')
        self.asa_hostels_menu = self.get_place_menu('Общежития', 'Общежитие')
        self.asa_sport_menu = self.get_place_menu('Спортивные комплексы', 'Спортивные комплексы')
        self.asa_other_places_menu = self.get_place_menu('Другое', 'Другое')

        self.dstu_menu.add_menu_item(self.dstu_housings_menu.name, self.asa_housings_menu)
        self.dstu_menu.add_menu_item(self.dstu_cafe_menu.name, self.asa_cafe_menu)
        self.dstu_menu.add_menu_item(self.dstu_hostels_menu.name, self.asa_hostels_menu)
        self.dstu_menu.add_menu_item(self.dstu_sport_menu.name, self.asa_sport_menu)
        self.dstu_menu.add_menu_item(self.dstu_other_places_menu.name, self.asa_other_places_menu)

        self.places_menu.add_menu_item('АСА', self.asa_menu)

        # Стипендии
        self.grants_menu = Menu('Стипендии')

        self.grants_mag = self.get_grants_menu('Магистратура', 'Магистратура')
        self.grants_bak = self.get_grants_menu('Бакалавриат', 'Бакалавриат')

        self.grants_bak.add_basic_item('Гос. академическая стипендия', "", self.get_grant_bak_academ)
        self.grants_bak.add_basic_item('Гос. академическая стипенд', "", self.get_grant_bak_up_academ)

        self.grants_menu.add_menu_item(self.grants_mag.name, self.grants_mag)
        self.grants_menu.add_menu_item(self.grants_bak.name, self.grants_bak)

        # Узнать расписание

        self.schedule_menu = Menu('Узнать расписание')

        self.schedule_menu.add_special_item('Мое расписание', "", [('Я не знаю вашу группу\n' \
                                                                    'Введите название чтобы я запомнил\n' \
                                                                    'Например ВПР41 или вПр-41, как угодно :)', None)],
                                            lambda *args: None)

        self.schedule_menu.add_special_item('Расписание группы', "", [('Введите название чтобы я запомнил\n' \
                                                                       'Например ВПР41 или вПр-41, как угодно :)',
                                                                       None)],
                                            lambda *args: None)

        # Факультеты и кафедры

        self.faculties_and_departments_menu = Menu('Факультеты и кафедры')
        self.faculties_menu = Menu('Факультеты')
        self.departments_menu = Menu('Кафедры')
        self.specialty = Menu('Направления')

        # self.specialty.add_basic_item('Программная инженерия', '', self.pi_specialty)
        # self.specialty.add_basic_item('Компьютерная безопасность', '', self.pi_specialty)
        # self.specialty.add_basic_item('Прикладная математика', '', self.pi_specialty)

        # self.departments_menu.add_basic_item('ПОВТиАС', '', self.povtias_department)
        # self.departments_menu.add_menu_item(self.specialty.name, self.specialty)
        #
        # self.faculties_menu.add_basic_item('ИиВТ', '', self.iivt_faculty)
        # self.faculties_menu.add_menu_item(self.departments_menu.name, self.departments_menu)
        # self.faculties_menu.add_basic_item('МКиМТ', '', self.mkmt_faculty)
        # self.faculties_menu.add_basic_item('АМиУ', '', self.amiu_faculty)

        self.faculties_and_departments_menu.add_menu_item(self.faculties_menu.name, self.faculties_menu)
        self.faculties_and_departments_menu.add_menu_item(self.departments_menu.name, self.departments_menu)

        # Настройки

        self.settings_menu = Menu('Настройки')

        self.root.add_menu_item(self.places_menu.name, self.places_menu)
        self.root.add_menu_item(self.schedule_menu.name, self.schedule_menu)
        self.root.add_menu_item(self.faculties_and_departments_menu.name, self.faculties_and_departments_menu)
        self.root.add_menu_item(self.grants_menu.name, self.grants_menu)
        self.root.add_menu_item(self.settings_menu.name, self.settings_menu)
        self.root.add_special_item("Оставить отзыв или предложение", "", [('Введите ваше предложение:', None)],
                                   lambda *args: None)
        self.root.add_basic_item("О Боте", "", self.about_me)

    def get_format_place(self, name):
        place = self.placeDAO.get_place_by_name(name)
        if not place:
            return 'Извините, запрашевоемое место еще не добавлено'
        result = "Название: " + place.name + "\n"
        if place.adress:
            result += "📍Адрес: " + place.adress + "\n"
        if place.managers:
            result += "👤Управляющие: " + ''.join(i.first_name for i in place.managers) + "\n"
        if place.phones:
            result += "📞Телефоны: " + ', '.join(i.phone for i in place.phones) + "\n"
        if place.schedules:
            result += "🕗Расписание: \n" + '\n'.join(
                '%s: %s - %s' % (
                    i.day_of_week.name, i.start_time.strftime("%H:%M"), i.end_time.strftime("%H:%M"))
                for i in place.schedules) + "\n"
        if place.map_url:
            result += "Карта: " + place.map_url + "\n"
        return (result, place.img_name)

    def get_place_menu(self, button_name: str, place_type: str):
        menu = Menu(button_name)
        for place in self.placeDAO.get_place_by_type(place_type):
            menu.add_basic_item(place.name, "", lambda **kwargs: self.get_format_place(kwargs['request']))
        return menu

    def get_format_grant(self, name):
        grant = self.grantDAO.get_place_by_name(name)
        if not grant:
            return 'Извините, запрашевоемое место еще не добавлено'
        result = 'Название: ' + grant.name + '\n'

        result += '📄 Условия получения:\n'
        for condition in grant.conditions:
            result += '  - '+condition.description + '\n'

        result += '\n💶 Размеры выплат:\n'
        for payment in grant.payments:
            result += '  - '+payment.conditions + (' в т.ч. ИГ' if payment.foreigner else '') + '  - ' + str(payment.money) + 'р\n'

        result += '\n*ИГ - иностранные граждане'

        return result, None

    def get_grant_bak_academ(self):
        return 'Название: Государственная академическая стипендия\n' \
               '📄 Условия получения:\n' \
               '- Отсутствие по итогам сессии оценки ниже 4 и отсутствие задолжностей;\n' \
               '- Являетесь иностранным гражданином\n' \
               '- Обучаетесь на 1 курсе 1 семестре\n' \
               '💶 Размеры выплат:\n' \
               '- 1 курс 1 семестр - 1700\n' \
               '- Иностранным гражданам - 1700\n' \
               '- Сессия закрыта на "хорошо" в т.ч. ИГ - 2700\n' \
               '- Сессия закрыта на "хорошо" в т.ч. ИГ и "отлично" - 3100\n' \
               '- Сессия закрыта на и "отлично" в т.ч. ИГ - 3500\n\n' \
               '*ИГ - иностранные граждане'

    def get_grant_bak_up_academ(self):
        return 'Название: Повышенная государственная академическая стипендия\n' \
               '📄 Условия получения:\n' \
               '- За достижения в учебной деятельности' \
               ' a) Получение в течении 2-х последних сессий только оценки "отлично";\n' \
               ' б) Получение в течение последнего года награды за результаты проектной деятельности;\n' \
               ' в) Признание студента победителем или призером международной,  всероссийской, региональной или ' \
               'ведомственной олимпиады/конкурса/соревнования.\n\n' \
               '- За достижения в научно-исследовательской деятельности' \
               ' a) Получение в течение последнего года награды или документа за результаты научно-исследовательской работы;\n' \
               ' б) Наличие в течении последнего года публикации в научном международном, всероссийском, региональном или ведомственном издании;\n\n' \
               '- За достижения в общественной деятельности\n' \
               ' a) Систематическое участие в течении последнего года в проведении мироприятий социального, культурного ' \
               'или общественного характера, организуемой ДГТУ или с его участием и подтвержаемое документально;\n' \
               ' б) Систематическое участие в течении последнего года в деятельности по информационному обеспечению ' \
               'общественно значимых мероприятий, общественной жизни университета, подтверждаемое документально;\n\n' \
               '- За достижения в культурно-творческой деятельности\n' \
               ' a) Получение в течение последнего года награды за результаты культурно-творческой деятельности ' \
               'проводимой университетом или другой организации, подтвержденное документально;\n' \
               ' б) Публичное представление в течении последнего года произведение искусства (литературное, музыкальное,' \
               'сценарное, хореографического произведения, а также комикса, рассказа, картины, фотографии, геологической' \
               ' или другой карты, плана, эскиза) подтвержденное документально;\n' \
               ' в) Систематическое участие в течении последнего года в проведении культурно-творческой деятельности' \
               ' воспитательного или пропагандистского харрактера;\n\n' \
               '- За достижения в спортивной деятельности\n' \
               ' a) Получение в течение последнего года награды за результаты спортивной деятельности ' \
               'осуществляемой им в рамках международных, всероссийских, региональных или ведомственных мероприятий' \
               'проводимых университетом или иной организацией;\n' \
               ' б) Систематическое участие в течении последнего года в спортивных мероприятиях воспитательного или ' \
               'пропагандистского характера подтверждаемое документально;\n' \
               ' в) выполнение нормативов и требований золотого знака отличия (ГТО) соответствующей возрастной группы' \
               ' на дату назначения стипендии;\n\n' \
               '💶 Размеры выплат:\n' \
               '- 2 курс в т.ч. ИГ - 10500\n' \
               '- 3 курс в т.ч. ИГ - 11000\n' \
               '- 4,5,6 курс в т.ч. ИГ - 12000\n' \
               '*ИГ - иностранные граждане'

    def get_grant_mag_up_academ(self):
        return 'Название: Повышенная государственная академическая стипендия\n' \
               '📄 Условия получения:\n' \
               '- За достижения в учебной деятельности' \
               ' a) Получение в течении 2-х последних сессий только оценки "отлично";\n' \
               ' б) Получение в течение последнего года награды за результаты проектной деятельности;\n' \
               ' в) Признание студента победителем или призером международной,  всероссийской, региональной или ' \
               'ведомственной олимпиады/конкурса/соревнования.\n\n' \
               '- За достижения в научно-исследовательской деятельности' \
               ' a) Получение в течение последнего года награды или документа за результаты научно-исследовательской работы;\n' \
               ' б) Наличие в течении последнего года публикации в научном международном, всероссийском, региональном или ведомственном издании;\n\n' \
               '- За достижения в общественной деятельности\n' \
               ' a) Систематическое участие в течении последнего года в проведении мироприятий социального, культурного ' \
               'или общественного характера, организуемой ДГТУ или с его участием и подтвержаемое документально;\n' \
               ' б) Систематическое участие в течении последнего года в деятельности по информационному обеспечению ' \
               'общественно значимых мероприятий, общественной жизни университета, подтверждаемое документально;\n\n' \
               '- За достижения в культурно-творческой деятельности\n' \
               ' a) Получение в течение последнего года награды за результаты культурно-творческой деятельности ' \
               'проводимой университетом или другой организации, подтвержденное документально;\n' \
               ' б) Публичное представление в течении последнего года произведение искусства (литературное, музыкальное,' \
               'сценарное, хореографического произведения, а также комикса, рассказа, картины, фотографии, геологической' \
               ' или другой карты, плана, эскиза) подтвержденное документально;\n' \
               ' в) Систематическое участие в течении последнего года в проведении культурно-творческой деятельности' \
               ' воспитательного или пропагандистского харрактера;\n\n' \
               '- За достижения в спортивной деятельности\n' \
               ' a) Получение в течение последнего года награды за результаты спортивной деятельности ' \
               'осуществляемой им в рамках международных, всероссийских, региональных или ведомственных мероприятий' \
               'проводимых университетом или иной организацией;\n' \
               ' б) Систематическое участие в течении последнего года в спортивных мероприятиях воспитательного или ' \
               'пропагандистского характера подтверждаемое документально;\n' \
               ' в) выполнение нормативов и требований золотого знака отличия (ГТО) соответствующей возрастной группы' \
               ' на дату назначения стипендии;\n\n' \
               '💶 Размеры выплат:\n' \
               '- Все куртсы в т.ч. ИГ - 14000\n\n' \
               '*ИГ - иностранные граждане'

    def get_grant_mag_academ(self):
        return 'Название: Государственная академическая стипендия\n' \
               '📄 Условия получения:\n' \
               '- Отсутствие по итогам сессии оценки ниже 4 и отсутствие задолжностей;\n' \
               '- Являетесь иностранным гражданином\n' \
               '- Обучаетесь на 1 курсе 1 семестре\n' \
               'иностранные граждане и)\n\n' \
               '💶 Размеры выплат:\n' \
               '- 1 курс 1 семестр - 3000\n' \
               '- Иностранным гражданам - 3000\n' \
               '- Сессия закрыта на "хорошо" в т.ч. ИГ - 3500\n' \
               '- Сессия закрыта на "хорошо" в т.ч. ИГ и "отлично" - 3750\n' \
               '- Сессия закрыта на и "отлично" в т.ч. ИГ - 4100\n\n' \
               '*ИГ - иностранные граждане'

    def get_grants_menu(self, button_name: str, form_of_study: str):
        menu = Menu(button_name)
        for grant in self.grantDAO.get_grant_by_type(form_of_study):
            menu.add_basic_item(grant.name, "", lambda **kwargs: self.get_format_grant(kwargs['request']))
        return menu

    def about_me(self, **kwargs):
        return ("Я помогу узнать необходимую для тебя информацию о ДГТУ. " \
                "Помогу найти нужный корпус и узнать подробную информацию о разных местах. " \
                "Спрашивай, не стесняйся!&#128521;", None)
