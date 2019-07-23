from app.models.models import Place, Faculty, User
from app.models.models_menu import Menu
from app import answer_functions as spec_foo


class MenuTree:

    def __init__(self):
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
                                                                    'Например ВПР41 или вПр-41, как угодно :)', None)],
                                            lambda *args, **kwargs: ('222', None))

        self.schedule_menu.add_special_item('Расписание группы', "Мое расписание", [('Введите название чтобы я запомнил\n' \
                                                                       'Например ВПР41 или вПр-41, как угодно :)',
                                                                       None)],
                                            lambda *args, **kwargs: ('111', None))

        # Факультеты и кафедры

        self.faculties_and_departments_menu = Menu('Факультеты и кафедры')
        self.faculties_menu = self.get_faculty_menu('Факультеты')
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
        self.root.add_special_item("Оставить отзыв или предложение", "Оставить отзыв или предложение", [('Введите ваше предложение:', None)],
                                   self.add_sentence)
        self.root.add_basic_item("О Боте", "", spec_foo.about_me)

    def add_sentence(self, *args, **kwargs):
        User.get_user(kwargs['vk_id']).add_review(kwargs['list_answers'][0])
        return 'Спасибо за отзыв😊', None


    def get_format_place(self, name):
        place = Place.get_place(name)
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
        faculty = Faculty.get_faculty(name, abbreviation)
        if not faculty:
            return 'Извините, запрашевоемое место еще не добавлено', None
        result = "Название: " + faculty.name + "\n"
        if faculty.abbreviation:
            result += "Аббревиатура: %s\n" % faculty.abbreviation
        if faculty.phone:
            result += "📞Телефон: %s\n" % faculty.phone
        if faculty.dean:
            result += "👤Декан: %s %s %s\n" % (faculty.dean.last_name, faculty.dean.first_name, faculty.dean.patronymic)
        if faculty.cabinet_dean:
            result += "📍Кабинет декана: %s\n" % faculty.cabinet_dean
        if faculty.cabinet_dean_office:
            result += "📍Кабинет деканата: %s\n" % faculty.cabinet_dean_office
        if faculty.schedules:
            result += "🕗Расписание деканата: \n" + '\n'.join(
                '%s: %s - %s' % (
                    i.day_of_week, i.start_time.strftime("%H:%M"), i.end_time.strftime("%H:%M"))
                for i in faculty.schedules) + "\n"
        return result, None

    def get_place_menu(self, button_name: str, place_type: str):
        menu = Menu(button_name)
        for place in Place.get_places_by_type(place_type):
            menu.add_basic_item(place.name, "", lambda **kwargs: self.get_format_place(kwargs['request']))
        return menu

    def get_departments(self, faculty_name):
        menu = Menu('Кафедры факультета')
        menu.add_basic_item('Какая-то кафедра', "", lambda **kwargs: ('инфа', None))
        return menu

    def get_specialties(self, faculty_name):
        menu = Menu('Специальности факультета')
        menu.add_basic_item('Какая-то специальность', "", lambda **kwargs: ('инфа', None))
        return menu

    def get_abbreviation_lambda(self, faculty):
        return lambda **kwargs: self.get_format_faculty(name=faculty.name)

    def get_faculty_menu(self, button_name: str):
        menu = Menu(button_name)

        for faculty in Faculty.all():
            menu_faculty = Menu(faculty.abbreviation if faculty.abbreviation else faculty.name)
            menu_faculty.add_basic_item('Информация о факультете', '', self.get_abbreviation_lambda(faculty))

            departments_of_faculty = self.get_departments(faculty.name)
            menu_faculty.add_menu_item(departments_of_faculty.name, departments_of_faculty)

            specialties_of_faculty = self.get_specialties(faculty.name)
            menu_faculty.add_menu_item(specialties_of_faculty.name, specialties_of_faculty)

            # menu_faculty.add_menu_item('Направления', self.get_department)
            menu.add_menu_item(menu_faculty.name, menu_faculty)

        return menu
