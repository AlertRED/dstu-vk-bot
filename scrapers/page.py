from time import sleep

from scrapers.scraper_schedule import ScrapePage
from app.models.models_schedule import Group, Subject

numbers = {'8-30': 1, '10-15': 2, '12-00': 3, '14-15': 4, '16-00': 5, '17-45': 6, '19:30': 7}
days = {'Понедельник': 'пн',
        'Вторник': 'вт',
        'Среда': 'ср',
        'Четверг': 'чт',
        'Пятница': 'пт',
        'Суббота': 'сб',
        'Воскресенье': 'вс'}

scraper = ScrapePage()

# Sum：1957
# Start: 31884
# End: 33841

# ВПР41 - 32342

errors = 0
for i in range(32342, 32343):
    i -= errors
    try:
        data = scraper.get_schedule(str(i))
    except:
        print('continue')
        errors += 1
        continue
    log = '%s: %s ' % (str(i), data[1] if data else '')
    if not data or data[0] != '2019-2020' or len(data[3]) == 0:
        print(log + 'False')
        continue

    group = Group.create(name=data[1], year=data[0], number_by_site=i, semester=1)
    for day in data[3]:
        if not day['day_name'] in days.keys():
            continue
        time = ''
        for item in day['schedule']:
            correct_index = 0
            if numbers.get(item[0]):
                time = item[0]
            else:
                correct_index = -1
            if item[-1] in ('Н нед.', '*'):
                subject = Subject.create(item[correct_index + 1], numbers[time], 1, 1, days[day['day_name']])
                try:
                    first_name, last_name, patronymic = item[correct_index + 2].replace(' ', '.').split('.')[:3]
                except ValueError:
                    first_name, last_name, patronymic = None, None, None
                subject.set_teacher(first_name, last_name, patronymic)
                group.add_subject(subject)
                print(subject)
            if item[-1] in ('В нед.', '*'):
                subject = Subject.create(item[correct_index + 1], numbers[time], 2, 1, days[day['day_name']])
                try:
                    first_name, last_name, patronymic = item[correct_index + 2].replace(' ', '.').split('.')[:3]
                except ValueError:
                    first_name, last_name, patronymic = None, None, None
                subject.set_teacher(first_name, last_name, patronymic)
                group.add_subject(subject)
                print(subject)

    print(log + 'True')

# print(Group.get_group('ВПР41').get_schedule(day='пн'))


