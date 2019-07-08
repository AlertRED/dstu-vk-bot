from sqlalchemy.orm import Session
from app.models.models import db, Place
from app.daos.place_dao import placeDAO

db = Session(bind=db)
placeDAO = placeDAO(db)

Place.create('Главный корпус',
             map_url='https://www.google.com/maps/place/%D0%94%D0%93%D0%A2%D0%A3/@47.2372723,39.7116784,19.1z/data=!4m8!1m2!2m1!1z0LrQsNGA0YLRiw!3m4!1s0x40e3bbd25efc8dab:0xe71795934da757ba!8m2!3d47.2373015!4d39.7121356?hl=ru',
             adress='пл. Гагарина, 1',
             img_name='главный_корпус.jpg'
             ).add_type_place('Корпус'). \
    set_phones(['88632738566']). \
    add_schedule('пн', '8:10', '21:00'). \
    add_schedule('вт', '8:10', '21:00'). \
    add_schedule('ср', '8:10', '21:00'). \
    add_schedule('чт', '8:10', '21:00'). \
    add_schedule('пт', '8:10', '21:00'). \
    add_schedule('сб', '8:10', '21:00')

Place.create('Корпус №2',
             map_url='https://www.google.com/maps/place/%D0%A0%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%BD%D1%8B%D0%B9+%D1%86%D0%B5%D0%BD%D1%82%D1%80+%D1%80%D0%BE%D0%B1%D0%BE%D1%82%D0%BE%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B8+%D0%94%D0%93%D0%A2%D0%A3/@47.2384843,39.7124435,19z/data=!4m8!1m2!2m1!1z0LrQsNGA0YLRiw!3m4!1s0x40e3b9ac5cb77cab:0x95283ab2e3f66212!8m2!3d47.2385107!4d39.7129022?hl=ru',
             adress='пр. Михаила Нагибина, 3а',
             img_name='корпус_2.jpg'
             ).add_type_place('Корпус'). \
    set_phones(['88632381539']). \
    add_schedule('пн', '8:10', '21:00'). \
    add_schedule('вт', '8:10', '21:00'). \
    add_schedule('ср', '8:10', '21:00'). \
    add_schedule('чт', '8:10', '21:00'). \
    add_schedule('пт', '8:10', '21:00'). \
    add_schedule('сб', '8:10', '21:00')

Place.create('Корпус №8',
             map_url='https://www.google.com/maps/place/%D0%A3%D1%87%D0%B5%D0%B1%D0%BD%D0%BE-%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D1%8B%D0%B9+%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81+%E2%84%96+8/@47.2379222,39.7109109,19.1z/data=!4m8!1m2!2m1!1z0LrQsNGA0YLRiw!3m4!1s0x0:0x7718a6501d7dfc82!8m2!3d47.2380107!4d39.7109641?hl=ru',
             adress='пл. Гагарина, 1',
             img_name='корпус_8.jpg'
             ).add_type_place('Корпус'). \
    set_phones(['88632738511']). \
    add_schedule('пн', '8:10', '21:00'). \
    add_schedule('вт', '8:10', '21:00'). \
    add_schedule('ср', '8:10', '21:00'). \
    add_schedule('чт', '8:10', '21:00'). \
    add_schedule('пт', '8:10', '21:00'). \
    add_schedule('сб', '8:10', '21:00')

Place.create('Корпус №3,4,5',
             map_url='https://www.google.com/maps/place/%D0%A3%D1%87%D0%B5%D0%B1%D0%BD%D0%BE-%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D1%8B%D0%B5+%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81%D0%B0+%E2%84%96+3,+4,+5/@47.2381465,39.71003,19.1z/data=!4m8!1m2!2m1!1z0LrQsNGA0YLRiw!3m4!1s0x0:0x92d4fa6c4ce0e552!8m2!3d47.2383324!4d39.7095948?hl=ru',
             adress='пл. Гагарина, 1',
             img_name='корпус_3_4_5.jpg'
             ).add_type_place('Корпус'). \
    set_phones(['88632738511']). \
    add_schedule('пн', '8:10', '21:00'). \
    add_schedule('вт', '8:10', '21:00'). \
    add_schedule('ср', '8:10', '21:00'). \
    add_schedule('чт', '8:10', '21:00'). \
    add_schedule('пт', '8:10', '21:00'). \
    add_schedule('сб', '8:10', '21:00')

Place.create('Конгресс-Холл',
             map_url='https://www.google.com/maps/place/%D0%9A%D0%BE%D0%BD%D0%B3%D1%80%D0%B5%D1%81%D1%81-%D0%A5%D0%BE%D0%BB%D0%BB/@47.2377335,39.7124364,18.41z/data=!4m8!1m2!2m1!1z0LrQsNGA0YLRiw!3m4!1s0x40e3b9ac6e670b53:0xa0cee54076710c3f!8m2!3d47.2378533!4d39.7124118?hl=ru',
             adress='пл. Гагарина, 1',
             img_name='конгресс-холл.jpg'
             ).add_type_place('Корпус'). \
    set_phones(['88632381728']). \
    add_schedule('пн', '8:10', '21:00'). \
    add_schedule('вт', '8:10', '21:00'). \
    add_schedule('ср', '8:10', '21:00'). \
    add_schedule('чт', '8:10', '21:00'). \
    add_schedule('пт', '8:10', '21:00'). \
    add_schedule('сб', '8:10', '21:00')

Place.create('Корпус №6,7',
             map_url='https://vk.com/away.php?to=https%3A%2F%2Fwww.google.com%2Fmaps%2Fplace%2F%CC%E5%E4%E8%E0%EF%E0%F0%EA%2B%DE%E6%ED%FB%E9%2B%D0%E5%E3%E8%EE%ED%2C%2F%4047.2383522%2C39.7115657%2C19z%2Fdata%3D%214m8%211m2%212m1%211z0LrQsNGA0YLRiw%213m4%211s0x40e3b9ac1572738b%3A0x8243af72d94e08be%218m2%213d47.2383236%214d39.7121389%3Fhl%3Dru&cc_key=',
             adress='пл. Гагарина, 1',
             img_name='корпус_6_7.jpg'
             ).add_type_place('Корпус'). \
    add_schedule('пн', '8:10', '21:00'). \
    add_schedule('вт', '8:10', '21:00'). \
    add_schedule('ср', '8:10', '21:00'). \
    add_schedule('чт', '8:10', '21:00'). \
    add_schedule('пт', '8:10', '21:00'). \
    add_schedule('сб', '8:10', '21:00')


#####################################################################################

Place.create('Общежитие №1',
             map_url='https://www.google.com/maps/place/%D0%9E%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D0%B5+%E2%84%96+1/@47.2601314,39.7718087,18.79z/data=!4m8!1m2!2m1!1z0LTQs9GC0YMg0L7QsdGJ0LXQttC40YLQuNC1IDE!3m4!1s0x0:0xf9aa82fca57c90da!8m2!3d47.2598809!4d39.7720541',
             adress='Студенческая ул., 2',
             img_name='общежитие_1.jpg'
             ).add_type_place('Общежитие'). \
    set_phones(['88632521578']).\
    add_schedule('пн', '6:00', '00:00'). \
    add_schedule('вт', '6:00', '00:00'). \
    add_schedule('ср', '6:00', '00:00'). \
    add_schedule('чт', '6:00', '00:00'). \
    add_schedule('пт', '6:00', '00:00'). \
    add_schedule('сб', '6:00', '00:00').\
    add_schedule('вс', '6:00', '00:00')

Place.create('Общежитие №2',
             map_url='https://www.google.com/maps/place/%D0%9E%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D0%B5+%E2%84%96+2,+%D0%94%D0%93%D0%A2%D0%A3/@47.2394435,39.7107955,17z/data=!4m12!1m6!3m5!1s0x40e3b9acff0b1333:0xc83452710ceb0a5c!2z0J7QsdGJ0LXQttC40YLQuNC1IOKEliAyLCDQlNCT0KLQow!8m2!3d47.2394399!4d39.7129842!3m4!1s0x40e3b9acff0b1333:0xc83452710ceb0a5c!8m2!3d47.2394399!4d39.7129842',
             adress='пр. Михаила Нагибина, 5',
             img_name='общежитие_2.jpg'
             ).add_type_place('Общежитие'). \
    set_phones(['88632327893']).\
    add_schedule('пн', '6:00', '00:00'). \
    add_schedule('вт', '6:00', '00:00'). \
    add_schedule('ср', '6:00', '00:00'). \
    add_schedule('чт', '6:00', '00:00'). \
    add_schedule('пт', '6:00', '00:00'). \
    add_schedule('сб', '6:00', '00:00').\
    add_schedule('вс', '6:00', '00:00')

Place.create('Общежитие №3',
             map_url='https://www.google.com/maps/place/%D0%9E%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D0%B5+%E2%84%96+3+%D0%94%D0%93%D0%A2%D0%A3/@47.2374266,39.707875,17z/data=!3m1!4b1!4m5!3m4!1s0x40e3b9ab830659cd:0x9e59e3612bedb1fe!8m2!3d47.237423!4d39.7100637',
             adress='ул. Мечникова, 79А',
             img_name='общежитие_3.jpg'
             ).add_type_place('Общежитие'). \
    set_phones(['88632738706']).\
    add_schedule('пн', '6:00', '00:00'). \
    add_schedule('вт', '6:00', '00:00'). \
    add_schedule('ср', '6:00', '00:00'). \
    add_schedule('чт', '6:00', '00:00'). \
    add_schedule('пт', '6:00', '00:00'). \
    add_schedule('сб', '6:00', '00:00').\
    add_schedule('вс', '6:00', '00:00')

Place.create('Общежитие №4',
             map_url='https://www.google.com/maps/place/%D0%9E%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D0%B5+%D0%94%D0%93%D0%A2%D0%A3+%E2%84%96+4/@47.235988,39.7083772,17z/data=!3m1!4b1!4m5!3m4!1s0x40e3b9168d1bf1fb:0x1be331da41f03be9!8m2!3d47.2359844!4d39.7105659',
             adress='ул. Текучева, 145',
             img_name='общежитие_4.jpg'
             ).add_type_place('Общежитие'). \
    set_phones(['88632738342']).\
    add_schedule('пн', '6:00', '00:00'). \
    add_schedule('вт', '6:00', '00:00'). \
    add_schedule('ср', '6:00', '00:00'). \
    add_schedule('чт', '6:00', '00:00'). \
    add_schedule('пт', '6:00', '00:00'). \
    add_schedule('сб', '6:00', '00:00').\
    add_schedule('вс', '6:00', '00:00')

Place.create('Общежитие №5',
             map_url='https://www.google.com/maps/place/%D0%9E%D0%B1%D1%89%D0%B5%D0%B6%D0%B8%D1%82%D0%B8%D0%B5+%D0%94%D0%93%D0%A2%D0%A3+%E2%84%96+5/@47.2364123,39.7078762,17z/data=!3m1!4b1!4m5!3m4!1s0x40e3b9abbdc2e5ad:0x555aeb683037be07!8m2!3d47.2364087!4d39.7100649',
             adress='ул. Мечникова, 154а',
             img_name='общежитие_5.jpg'
             ).add_type_place('Общежитие'). \
    set_phones(['88632381515']).\
    add_schedule('пн', '6:00', '00:00'). \
    add_schedule('вт', '6:00', '00:00'). \
    add_schedule('ср', '6:00', '00:00'). \
    add_schedule('чт', '6:00', '00:00'). \
    add_schedule('пт', '6:00', '00:00'). \
    add_schedule('сб', '6:00', '00:00').\
    add_schedule('вс', '6:00', '00:00')

#########################################################################################################

Place.create('Кафе "Экспресс"',
             map_url=None,
             adress='Корпус №8 (цоколь)',
             img_name='кафе_экспресс.jpg'
             ).add_type_place('Кафе'). \
    set_phones(['88632381515']).\
    add_schedule('пн', '8:30', '17:00'). \
    add_schedule('вт', '8:30', '17:00'). \
    add_schedule('ср', '8:30', '17:00'). \
    add_schedule('чт', '8:30', '17:00'). \
    add_schedule('пт', '8:30', '17:00')

Place.create('Кафе "Русь"',
             map_url='https://www.google.com/maps/place/%D0%9A%D0%B0%D1%84%D0%B5+%D0%A0%D1%83%D1%81%D1%8C/@47.236074,39.7103324,18z/data=!3m1!4b1!4m8!1m2!2m1!1z0LrQsNGE0LUg0Y3QutGB0L_RgNC10YHRgSDQtNCz0YLRgw!3m4!1s0x40e3b9abc1f322e5:0xb37f2c93d0a92847!8m2!3d47.236073!4d39.7109099',
             adress='ул. Текучева, 145',
             img_name='кафе_русь.jpg'
             ).add_type_place('Кафе'). \
    set_phones(['88632381512']).\
    add_schedule('пн', '8:30', '17:30'). \
    add_schedule('вт', '8:30', '17:30'). \
    add_schedule('ср', '8:30', '17:30'). \
    add_schedule('чт', '8:30', '17:30'). \
    add_schedule('пт', '8:30', '17:30')

Place.create('Кафе "Миг"',
             map_url=None,
             adress='Главный корпус, между 1 и 2 этажами',
             img_name='кафе_миг.jpg'
             ).add_type_place('Кафе'). \
    add_schedule('пн', '9:00', '17:00'). \
    add_schedule('вт', '9:00', '17:00'). \
    add_schedule('ср', '9:00', '17:00'). \
    add_schedule('чт', '9:00', '17:00'). \
    add_schedule('пт', '9:00', '17:00')


##############################################################################

Place.create('Спортивный манеж',
             map_url='https://www.google.com/maps/place/%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9+%D0%BC%D0%B0%D0%BD%D0%B5%D0%B6+%D0%94%D0%93%D0%A2%D0%A3/@47.2398909,39.7076387,16.51z/data=!4m8!1m2!2m1!1z0LTQs9GC0YMg0LvQtdCz0LrQvtCw0YLQu9C10YLQuNGH0LXRgdC60LjQuQ!3m4!1s0x0:0xc17d830a8a244c64!8m2!3d47.2410274!4d39.7091818',
             adress='ул. Юфимцева, 16',
             img_name='спортивный_манеж.jpg'
             ).add_type_place('Спортивные комплексы'). \
    set_phones(['88632324261']).\
    add_schedule('пн', '8:00', '20:00'). \
    add_schedule('вт', '8:00', '20:00'). \
    add_schedule('ср', '8:00', '20:00'). \
    add_schedule('чт', '8:00', '20:00'). \
    add_schedule('пт', '8:00', '20:00'). \
    add_schedule('сб', '8:00', '20:00'). \
    add_schedule('вс', '8:00', '20:00')

Place.create('Бассейн',
             map_url='https://www.google.com/maps/place/%D0%91%D0%B0%D1%81%D1%81%D0%B5%D0%B9%D0%BD+%D0%94%D0%93%D0%A2%D0%A3/@47.239151,39.7110635,17.17z/data=!4m8!1m2!2m1!1z0LTQs9GC0YMg0LvQtdCz0LrQvtCw0YLQu9C10YLQuNGH0LXRgdC60LjQuQ!3m4!1s0x0:0xc9f50ebde8d8614e!8m2!3d47.2387324!4d39.7109038',
             adress='пл. Гагарина, 1',
             img_name='бассейн.jpg'
             ).add_type_place('Спортивные комплексы'). \
    set_phones(['88632381335']).\
    add_schedule('пн', '7:00', '22:00'). \
    add_schedule('вт', '7:00', '22:00'). \
    add_schedule('ср', '7:00', '22:00'). \
    add_schedule('чт', '7:00', '22:00'). \
    add_schedule('пт', '7:00', '22:00'). \
    add_schedule('сб', '7:00', '22:00'). \
    add_schedule('вс', '8:00', '21:00')

Place.create('Футбольное поле',
             map_url='https://www.google.com/maps/place/%D0%A4%D1%83%D1%82%D0%B1%D0%BE%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5+%D0%BF%D0%BE%D0%BB%D0%B5+%D0%94%D0%93%D0%A2%D0%A3/@47.2387673,39.7088692,17z/data=!3m1!4b1!4m8!1m2!2m1!1z0LTQs9GC0YMg0LvQtdCz0LrQvtCw0YLQu9C10YLQuNGH0LXRgdC60LjQuQ!3m4!1s0x40e3b945d2445347:0xa81beb8e3d9ae2f8!8m2!3d47.238765!4d39.710248',
             adress='пл. Гагарина, 1 корпус 5',
             img_name='футбольное_поле.jpg'
             ).add_type_place('Спортивные комплексы')

########################################################################################

Place.create('Студенческий городок',
             map_url='https://www.google.com/maps/place/%D0%9F%D0%B0%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%BD%D1%8B%D0%B9+%D1%81%D1%82%D0%BE%D0%BB+%D1%81%D1%82%D1%83%D0%B4%D0%B5%D0%BD%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BA%D0%B0+%D0%94%D0%93%D0%A2%D0%A3/@47.2393242,39.7116183,18.09z/data=!4m8!1m2!2m1!1z0LTQs9GC0YMg0LvQtdCz0LrQvtCw0YLQu9C10YLQuNGH0LXRgdC60LjQuQ!3m4!1s0x0:0xbc80573f045d0914!8m2!3d47.2393163!4d39.7129989',
             adress='пр. Михаила Нагибина, 5',
             img_name='студенческий_городок.jpg'
             ).add_type_place('Другое'). \
    set_phones(['88632738580']).\
    add_schedule('пн', '9:00', '17:00'). \
    add_schedule('вт', '9:00', '17:00'). \
    add_schedule('ср', '9:00', '17:00'). \
    add_schedule('чт', '9:00', '17:00'). \
    add_schedule('пт', '9:00', '17:00'). \
    add_schedule('сб', '9:00', '17:00').\
    add_schedule('вс', '9:00', '17:00')

Place.create('Храм св.мч. Татианы',
             map_url='https://www.google.com/maps/place/%D0%A5%D1%80%D0%B0%D0%BC+%D1%81%D0%B2.%D0%BC%D1%87.+%D0%A2%D0%B0%D1%82%D0%B8%D0%B0%D0%BD%D1%8B+%D0%BF%D1%80%D0%B8+%D0%94%D0%93%D0%A2%D0%A3/@47.2387673,39.7088692,17z/data=!4m8!1m2!2m1!1z0LTQs9GC0YMg0LvQtdCz0LrQvtCw0YLQu9C10YLQuNGH0LXRgdC60LjQuQ!3m4!1s0x40e3b9acec26751f:0x11b612bba3e50f6!8m2!3d47.2392983!4d39.7111311',
             adress='пл. Гагарина, 1 корпус 5',
             img_name='храм.jpg'
             ).add_type_place('Другое'). \
    set_phones(['88632381528']).\
    add_schedule('пн', '7:00', '17:00'). \
    add_schedule('вт', '7:00', '17:00'). \
    add_schedule('ср', '7:00', '17:00'). \
    add_schedule('чт', '7:00', '17:00'). \
    add_schedule('пт', '7:00', '17:00'). \
    add_schedule('сб', '7:00', '17:00'). \
    add_schedule('вс', '7:00', '17:00')

