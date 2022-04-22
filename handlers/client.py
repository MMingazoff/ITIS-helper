from aiogram import types, Dispatcher
from keyboards.kb import *
from scripts import *
from exel_to_dataframe import df_student, list_group
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSM_start(StatesGroup):
    fio = State()
    menu = State()


class FSM_timetable(StatesGroup):
    timetable = State()
    today_tomorrow = State()
    someone_timetable = State()


class FSM_study(StatesGroup):
    study = State()
    subject = State()


class FSM_helps(StatesGroup):
    help = State()
    wishes = State()


class FSM_activity(StatesGroup):
    activity = State()
    events = State()
    someone_points = State()
    top_students = State()


class FSM_guid(StatesGroup):
    guid = State()


async def start_bot(message: types.Message):
    await message.answer('Привет! Я бот, который поможет тебе в студенческой жизни. Введи свое ФИО')
    await FSM_start.fio.set()


async def enter_FIO(message: types.Message):
    fio = message.text
    if any(df_student.ФИО == fio):
        course = 'n-ый'
        group = '***-**'
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \n Курс: {course} \n Группа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()
    else:
        await message.answer('Такого студента нету, или вы ошиблись ФИО')
        await FSM_start.fio.set()


async def menu(message: types.Message):
    if message.text == 'Расписание':
        await message.answer('Выбери расписание', reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()
    if message.text == 'Учеба':
        course = get_course('student_name')
        await message.answer('Выбери нужный тебе предмет', reply_markup=study_markup(course))
        await FSM_study.study.set()
    if message.text == 'Помощь':
        await message.answer('Чем помочь?', reply_markup=help_markup())
        await FSM_helps.help.set()
    if message.text == 'Сменить профиль':
        await FSM_start.fio.set()
        await message.answer('Введи свое ФИО')
    if message.text == 'Активности':
        await message.answer(
            'Здесь ты можешь посмотреть рейтинг, узнать свои баллы и узнать где можно заработать баллы',
            reply_markup=ativity_markup())
        await FSM_activity.activity.set()
    if message.text == 'Гид':
        await message.answer('Здесь ты можешь посмотреть места, где можно хорошо провести время',
                             reply_markup=guild_markup())
        await FSM_guid.guid.set()


async def timetable(message: types.Message):
    if message.text == 'Расписание на неделю':
        text = get_week_timetable(str(message.from_user))
        await message.answer(text)
    if message.text == 'Расписание на день':
        await message.answer('Выбери нужный день', reply_markup=todaytomorrow_markup())
        await FSM_timetable.today_tomorrow.set()
    if message.text == 'Какая у меня сейчас пара':
        text = get_now_lesson(str(message.from_user))
        await message.answer(text)
    if message.text == 'Узнать пары у другого человека':
        await message.answer('Введи номер группы или фамилию с именем', reply_markup=timetable_someone_markup())
        await FSM_timetable.someone_timetable.set()

    if message.text == 'Назад в меню':
        fio = 'Фамилия Имя Отчество'
        course = 'n-ый'
        group = '***-**'
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \n Курс: {course} \n Группа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()


async def timetable_day_lessons(message: types.Message):
    if message.text == 'Пары сегодня':
        text = get_today_lessons(str(message.from_user))
        await message.answer(text)
    if message.text == 'Пары завтра':
        text = get_tomorrow_lessons(str(message.from_user))
        await message.answer(text)
    if message.text == 'Вернуться в расписание':
        await message.answer('Выбери расписание', reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()


async def timetable_someone(message: types.Message):
    if any(df_student.ФИО == message.text):
        text = get_today_lessons(str(message.from_user))
        await message.answer(text, reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()
    elif message.text in list_group:
        text = get_today_lessons_by_group(message.text)
        await message.answer(text, reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()
    elif message.text == 'Вернуться в расписание':
        await message.answer('Выбери расписание', reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()

    else:
        await message.answer('Такого ученика/группы нету, попробуйте ввести заново')


async def subjects(message: types.Message):
    if message.text == 'Назад в меню':
        fio = 'Фамилия Имя Отчество'
        course = 'n-ый'
        group = '***-**'
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \n Курс: {course} \n Группа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()
    else:
        await message.answer('Пока думаем')


async def help(message: types.Message):
    if message.text == 'Список моей группы':
        ur_group = 'Тут должно быть фото твоей группы'
        await message.answer(ur_group)
    if message.text == 'Связь с деканатом':
        deanery = 'Тут вся связь с деканатом'
        await message.answer(deanery)
    if message.text == 'Список старост':
        elders = 'Тут должен быть список старост'
        await message.answer(elders)
    if message.text == 'Ваши пожелания для бота':
        await message.answer('Введите ваши пожелания', reply_markup=wishes_markup())
        await FSM_helps.wishes.set()
    if message.text == 'Вернуться в меню':
        fio = 'Фамилия Имя Отчество'
        course = 'n-ый'
        group = '***-**'
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \n Курс: {course} \n Группа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()


async def wishes(message: types.Message):
    # Тут надо добавить пожелание в БД
    if message.text == 'Вернуться в помощь':
        await message.answer('Чем помочь?', reply_markup=help_markup())
        await FSM_helps.help.set()
    else:
        await message.answer('Мы рассмотрим вашу идею', reply_markup=help_markup())
        await FSM_helps.help.set()


async def activity(message: types.Message):
    if message.text == 'Доступные мероприятия':
        await message.answer('Тут будет список свободных мероприятий', reply_markup=events_markup())
        await FSM_activity.events.set()
    if message.text == 'Я в рейтинге':
        ur_place = 'Тут будут твое место и твои баллы'
        await message.answer(ur_place)
    if message.text == 'Узнать баллы человека':
        await message.answer('Введите фамилию и имя человека', reply_markup=someone_points_markup())
        await FSM_activity.someone_points.set()
    if message.text == 'Общий рейтинг':
        await message.answer('Тут должен быть список студнтов с 1 по 10 место', reply_markup=top_students_markup())
        await FSM_activity.top_students.set()
    if message.text == 'Вернуться в меню':
        fio = 'Фамилия Имя Отчество'
        course = 'n-ый'
        group = '***-**'
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \n Курс: {course} \n Группа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()


async def events(message: types.Message):
    if message.text == 'Скопировать ФИО и группу':
        await message.answer('Копируешь свое фио')
    if message.text == 'Назад в активность':
        await message.answer(
            'Здесь ты можешь посмотреть рейтинг, узнать свои баллы и узнать где можно заработать баллы',
            reply_markup=ativity_markup())
        await FSM_activity.activity.set()


async def someone_points(message: types.Message):
    if any(df_student.ФИО == message.text):
        await message.answer(f'У {message.text} n баллов и он на k месте')
    elif message.text == 'Назад в активность':
        await message.answer(
            'Здесь ты можешь посмотреть рейтинг, узнать свои баллы и узнать где можно заработать баллы',
            reply_markup=ativity_markup())
        await FSM_activity.activity.set()
    else:
        await message.answer('Такого человека нету, введите фамилию и имя ещё раз')


async def top_students(message: types.Message):
    if message.text == '1-10 место':
        rating = 'Тут должен быть список студнтов с 1 по 10 место'
        await message.answer(rating)
    if message.text == '11-20 место':
        rating = 'Тут должен быть список студнтов с 11 по 20 место'
        await message.answer(rating)
    if message.text == '21-30 место':
        rating = 'Тут должен быть список студнтов с 21 по 30 место'
        await message.answer(rating)
    if message.text == 'Назад в активность':
        await message.answer(
            'Здесь ты можешь посмотреть рейтинг, узнать свои баллы и узнать где можно заработать баллы',
            reply_markup=ativity_markup())
        await FSM_activity.activity.set()


async def guid(message: types.Message):
    if message.text == 'Общепиты':
        catering = 'Тут должны быть общепиты'
        await message.answer(catering)
    if message.text == 'Места где можно отдохнуть':
        places_to_relax = 'Тут должны быть места для отдыха'
        await message.answer(places_to_relax)
    if message.text == 'Справочник для первокурсника':
        student_handbook = 'Тут будет что-то связанное с помощью студенту'
        await message.answer(student_handbook)
    if message.text == 'Вернуться в меню':
        fio = 'Фамилия Имя Отчество'
        course = 'n-ый'
        group = '***-**'
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \n Курс: {course} \n Группа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'], state="*")
    dp.register_message_handler(enter_FIO, state=FSM_start.fio)
    dp.register_message_handler(menu, state=FSM_start.menu)
    dp.register_message_handler(timetable, state=FSM_timetable.timetable)
    dp.register_message_handler(timetable_day_lessons, state=FSM_timetable.today_tomorrow)
    dp.register_message_handler(timetable_someone, state=FSM_timetable.someone_timetable)
    dp.register_message_handler(subjects, state=FSM_study.study)
    dp.register_message_handler(help, state=FSM_helps.help)
    dp.register_message_handler(wishes, state=FSM_helps.wishes)
    dp.register_message_handler(activity, state=FSM_activity.activity)
    dp.register_message_handler(events, state=FSM_activity.events)
    dp.register_message_handler(someone_points, state=FSM_activity.someone_points)
    dp.register_message_handler(top_students, state=FSM_activity.top_students)
    dp.register_message_handler(guid, state=FSM_guid.guid)
