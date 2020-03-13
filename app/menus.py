import app.models.models_DB as models
from app.models_menu import Menu, TypeItem
from app import answer_functions as spec_foo


class MenuTree:

    def __init__(self):
        self.max_items_per_slide = 7 * 4

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

        self.grants_mag = Menu('Магистратура')
        self.grants_bak = Menu('Бакалавриат')
        self.grants_college = Menu('Колледж')
        self.grants_asp = Menu('Аспирантура')

        self.grants_bak.add_basic_item('Академическая стипендия', "", spec_foo.get_grant_bak_academ)
        self.grants_bak.add_basic_item('Повыш. академ. стипендия', "", spec_foo.get_grant_bak_up_academ)
        self.grants_bak.add_basic_item('Стипендия Л.В. Красниченко', "", spec_foo.get_grant_bak_krasnichenko)
        self.grants_bak.add_basic_item('Стипендия Ученого совета', "", spec_foo.get_grant_bak_uchony_sovet)
        self.grants_bak.add_basic_item('Соц. стипендия', "", spec_foo.get_grant_bak_soc)
        self.grants_bak.add_basic_item('Повыш. соц. стипендия', "", spec_foo.get_grant_bak_up_soc)

        self.grants_mag.add_basic_item('Академическая стипендия', "", spec_foo.get_grant_mag_academ)
        self.grants_mag.add_basic_item('Соц. стипендия', "", spec_foo.get_grant_mag_up_academ)
        self.grants_mag.add_basic_item('Стипендия Л.В. Красниченко', "", spec_foo.get_grant_mag_krasnichenko)
        self.grants_mag.add_basic_item('Стипендия Ученого совета', "", spec_foo.get_grant_mag_uchony_sovet)

        self.grants_college.add_basic_item('Академическая стипендия', "", spec_foo.get_grant_college_academ)
        self.grants_college.add_basic_item('Соц. стипендия', "", spec_foo.get_grant_college_soc)

        self.grants_asp.add_basic_item('Стипендия аспирантам', "", spec_foo.get_grant_asp_asp)

        self.grants_menu.add_menu_item(self.grants_mag.name, self.grants_mag)
        self.grants_menu.add_menu_item(self.grants_bak.name, self.grants_bak)
        self.grants_menu.add_menu_item(self.grants_college.name, self.grants_college)
        self.grants_menu.add_menu_item(self.grants_asp.name, self.grants_asp)
        self.grants_menu.add_basic_item('Материальная помощь', '', spec_foo.get_grant_material_support)

        # Узнать расписание

        self.schedule_menu = Menu('Узнать расписание')

        self.schedule_menu.add_special_item('Мое расписание', "Мое расписание", [('Я не знаю вашу группу\n' \
                                                                                  'Введите название чтобы я запомнил\n' \
                                                                                  'Например ВПР41 или вПр-41, как угодно :)',
                                                                                  None)],
                                            self.save_group,
                                            prepare={'condition': lambda *args, **kwargs: models.User.get_user(
                                                kwargs['vk_id']).group_name,
                                                     'method': lambda *args, **kwargs: self.get_schedule_of_group(
                                                         list_answers=[models.User.get_user(
                                                             kwargs['vk_id']).group_name])})

        self.schedule_menu.add_special_item('Расписание группы', "Расписание группы",
                                            [('Введите название группы',
                                              None)],
                                            self.get_schedule_of_group)

        # Факультеты и кафедры

        self.faculties_and_departments_menu = Menu('Факультеты и кафедры')
        self.faculties_menu = self.get_faculty_menu('Факультеты', over_back=self.root)
        self.departments_menu = self.get_department_menu('Кафедры')
        self.specialty = Menu('Направления')

        self.faculties_and_departments_menu.add_menu_item(self.faculties_menu.name, self.faculties_menu)
        self.faculties_and_departments_menu.add_menu_item(self.departments_menu.name, self.departments_menu)

        # Настройки
        self.settings_menu = Menu('Настройки')
        self.settings_menu.add_special_item('Изменить название моей группы', "Изменить название моей группы",
                                            [('Введите название вашей группы\n' \
                                              'Например ВПР41 или вПр-41, как угодно :)',
                                              None)],
                                            self.save_group)

        self.settings_menu.add_basic_item('Отключить напоминания о парах', 'Отключить напоминания о парах',
                                          method=self.notify_change)

        self.root.add_menu_item(self.places_menu.name, self.places_menu)
        self.root.add_menu_item(self.schedule_menu.name, self.schedule_menu)
        self.root.add_menu_item(self.faculties_and_departments_menu.name, self.faculties_and_departments_menu)
        self.root.add_menu_item(self.grants_menu.name, self.grants_menu)
        self.root.add_menu_item(self.settings_menu.name, self.settings_menu)
        self.root.add_special_item("Оставить отзыв или предложение", "Оставить отзыв или предложение",
                                   [('Введите ваше предложение:', None)],
                                   self.add_sentence)
        self.root.add_basic_item("О Боте", "", spec_foo.about_me)

    @staticmethod
    def distribution_menu_items(items):
        row_len = 0
        result = 0
        results = []
        count_items_in_row = 0
        count_rows = 1
        limit_row_len = 30
        limit_items_in_row = 4
        limit_rows = 5
        for item in items:
            row_len += len(item)
            count_items_in_row += 1
            result += 1
            if not ((count_items_in_row == 0) or (
                    row_len + len(item) < limit_row_len and count_items_in_row < limit_items_in_row)):
                count_items_in_row = 0
                row_len = 0
                count_rows += 1
                if count_rows == limit_rows:
                    count_rows = 1
                    results.append(result)
        return results

    def pagination(foo):
        def wrapper(*args, **kwargs):
            menu = foo(*args, **kwargs)
            slices = MenuTree.distribution_menu_items(menu.items)
            count = 0
            next_menu = root = Menu(menu.name)
            over_back = kwargs.get('over_back')
            for i, item in enumerate(menu.items.items()):
                if count < len(slices) and i == slices[count]:
                    count += 1
                    a = Menu('Далее')
                    if over_back:
                        next_menu.add_menu_item(over_back.name, over_back, type_item=TypeItem.GATE, is_heir=False)
                    next_menu.add_menu_item(a.name, a, type_item=TypeItem.GATE)
                    next_menu = a
                next_menu.add_menu_item(index=item[0], menu=item[1][0], is_heir=item[1][1])
            next_menu.add_menu_item(over_back.name, over_back, type_item=TypeItem.GATE, is_heir=False)
            return root

        return wrapper

    def notify_change(self, *args, **kwargs):
        new_remind = not models.User.get_user(kwargs['vk_id']).remind
        models.User.get_user(kwargs['vk_id']).set_remind(new_remind)
        return 'Напоминания %s' % ('включены' if new_remind else 'отключены')

    def save_group(self, *args, **kwargs):
        if len(kwargs['list_answers']) > 0 and models.Group.get_group(kwargs['list_answers'][0]):
            models.User.get_user(kwargs['vk_id']).update(group_name=kwargs['list_answers'][0])
            return 'Я запомнил вашу группу. Поменять ее можно в настройках.', None
        return 'Я не знаю такую группу', None

    def get_schedule_of_group(self, *args, **kwargs):
        group = models.Group.get_group(kwargs['list_answers'][0])
        days = {'Понедельник': 'пн',
                'Вторник': 'вт',
                'Среда': 'ср',
                'Четверг': 'чт',
                'Пятница': 'пт',
                'Суббота': 'сб',
                'Воскресенье': 'вс'}
        if group:
            answer = '▫ Номер пары ▫ Название ▫ Кабинет ▫'
            answer += '\n⬆Верхняя неделя'
            for long, short in days.items():
                schedule = sorted(group.get_schedule(day=short, week=2), key=lambda x: x.number)
                if len(schedule) == 0:
                    continue
                answer += '\n➖' + long + '\n' + '\n'.join(
                    '№%i: %s' % (i.number, i.name) for i in schedule)
            answer += '\n⬇Нижняя неделя'
            for long, short in days.items():
                schedule = sorted(group.get_schedule(day=short, week=1), key=lambda x: x.number)
                if len(schedule) == 0:
                    continue
                answer += '\n➖' + long + '\n' + '\n'.join(
                    '№%i: %s' % (i.number, i.name) for i in schedule)
            return answer, None
        return 'Группа не найдена', None

    def add_sentence(self, *args, **kwargs):
        models.User.get_user(kwargs['vk_id']).add_review(kwargs['list_answers'][0])
        return 'Спасибо за отзыв😊', None

    ## формат вывода
    def get_format_place(self, name):
        place = models.Place.get_place(name)
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
                    i.day_of_week, i.start_time.strftime("%H:%M"), i.end_time.strftime("%H:%M"))
                for i in place.schedules) + "\n"
        if place.map_url:
            result += "Карта: " + place.map_url + "\n"
        return result, place.img_name

    def get_format_faculty(self, name=None, abbreviation=None):
        faculty = models.Faculty.get_faculty(name, abbreviation)
        if not faculty:
            return 'Извините, запрашевоемое место еще не добавлено', None
        result = "Название: " + faculty.name + "\n"
        if faculty.abbreviation:
            result += "Аббревиатура: %s\n" % faculty.abbreviation
        if faculty.phones:
            result += "📞Телефон: %s\n" % faculty.phones
        if faculty.dean:
            result += "👤Декан: %s %s %s\n" % (faculty.dean.last_name, faculty.dean.first_name, faculty.dean.patronymic)
        if faculty.cabinet_dean:
            result += "📍Кабинет декана: %s\n" % ', '.join(faculty.cabinet_dean)
        if faculty.cabinet_dean_office:
            result += "📍Кабинет деканата: %s\n" % ', '.join(faculty.cabinet_dean_office)
        if faculty.schedules:
            result += "🕗Расписание деканата: \n" + '\n'.join(
                '%s: %s - %s' % (
                    i.day_of_week, i.start_time.strftime("%H:%M"), i.end_time.strftime("%H:%M"))
                for i in faculty.schedules) + "\n"
        return result, None

    def get_format_department(self, name=None, abbreviation=None):
        department = models.Department.get_department(name, abbreviation)
        if not department:
            return 'Извините, запрашевоемое место еще не добавлено', None
        result = "Название: " + department.name + "\n"
        if department.abbreviation:
            result += "Аббревиатура: %s\n" % department.abbreviation
        if department.phones:
            result += "📞Телефон: %s\n" % ', '.join(department.phones)
        if department.manager:
            result += "👤Заведующий: %s %s %s\n" % (
                department.manager.last_name, department.manager.first_name, department.manager.patronymic)
        if department.cabinets:
            result += "📍Кабинет: %s\n" % ', '.join(department.cabinets)
        if department.schedules:
            result += "🕗Расписание кафедры: \n" + '\n'.join(
                '%s: %s - %s' % (
                    i.day_of_week, i.start_time.strftime("%H:%M"), i.end_time.strftime("%H:%M"))
                for i in department.schedules) + "\n"
        return result, None

    # генераторы меню
    def get_place_menu(self, button_name: str, place_type: str):
        menu = Menu(button_name)
        for place in models.Place.get_places_by_type(place_type):
            menu.add_basic_item(place.name, "", lambda **kwargs: self.get_format_place(kwargs['request']))
        return menu

    @pagination
    def get_faculty_menu(self, button_name: str, over_back=None):
        menu = Menu(button_name)

        faculties = models.Faculty.get_faculties()
        if faculties:
            # limit = limit_foo([i.abbreviation if i.abbreviation else i.name for i in faculties])
            for faculty in faculties:
                menu_faculty = Menu(faculty.abbreviation if faculty.abbreviation else faculty.name)
                menu_faculty.add_basic_item('Информация о факультете', '', self.get_faculty_lambda(faculty))

                departments_of_faculty = self.get_department_menu('Кафедры факультета', faculty)
                menu_faculty.add_menu_item(departments_of_faculty.name, departments_of_faculty)

                specialties_of_faculty = self.get_specialties(faculty.name)
                menu_faculty.add_menu_item(specialties_of_faculty.name, specialties_of_faculty)

                menu.add_menu_item(menu_faculty.name, menu_faculty)

            # next_menu = self.get_faculty_menu('Далее', start_index=start_index + limit, over_back=over_back, limit_foo=limit_foo)
            # if next_menu.items:
            #     if over_back:
            #         menu.add_menu_item(over_back.name, over_back, type_item=TypeItem.GATE, is_heir=False)
            #     menu.add_menu_item(next_menu.name, next_menu, type_item=TypeItem.GATE)
        return menu

    def get_department_menu(self, button_name: str, faculty: models.Faculty = None):
        menu = Menu(button_name)
        for department in models.Department.all(faculty):
            menu_department = Menu(department.abbreviation if department.abbreviation else department.name)
            menu_department.add_basic_item('Информация о кафедре', '', self.get_department_lambda(department))
            menu.add_menu_item(menu_department.name, menu_department)
        return menu

    ## остальное
    def get_specialties(self, faculty_name):
        menu = Menu('Специальности факультета')
        menu.add_basic_item('Какая-то специальность', "", lambda **kwargs: ('инфа', None))
        return menu

    def get_faculty_lambda(self, faculty):
        return lambda **kwargs: self.get_format_faculty(name=faculty.name)

    def get_department_lambda(self, department):
        return lambda **kwargs: self.get_format_department(name=department.name)
