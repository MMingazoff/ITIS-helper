from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def menu_markup():
    """Кнопки для меню"""
    timetable = KeyboardButton('Расписание')
    study = KeyboardButton('Учеба')
    helps = KeyboardButton('Помощь')
    change_prof = KeyboardButton('Сменить профиль')
    activity = KeyboardButton('Активности')
    guid = KeyboardButton('Гид')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(timetable, change_prof).row(study, activity).row(helps, guid)
    return keyboard


def timetable_markup():
    """Кнопки для расписания"""
    timetable_week = KeyboardButton('Расписание на неделю')
    what_lesson_now = KeyboardButton('Какая у меня сейчас пара')
    timetable_day = KeyboardButton('Расписание на день')
    timetable_group = KeyboardButton('Узнать пары у другого человека')
    back_to_menu = KeyboardButton('Назад в меню')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(timetable_week, timetable_day).row(what_lesson_now, timetable_group).row(back_to_menu)
    return keyboard


def study_markup(course: int):
    """Кнопки для учебы"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    back_to_menu = KeyboardButton('Назад в меню')
    course_dict = {
        'course_1': ['Инфа', 'Матан', 'Алгем'],
        'course_2': ['Тик'],
        'course_3': ['ML', 'DL'],
        'course_4': ['Django', 'SQL']}
    course = 'course_' + str(course)
    for kb in course_dict[course]:
        keyboard.row(KeyboardButton(kb))

    keyboard.row(back_to_menu)
    return keyboard


def help_markup():
    """Кнопки для помощи"""
    list_group = KeyboardButton('Список моей группы')
    deanery = KeyboardButton('Связь с деканатом')
    elders = KeyboardButton('Список старост')
    wishes = KeyboardButton('Ваши пожелания для бота')
    back_to_menu = KeyboardButton('Вернуться в меню')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(list_group, elders).row(deanery, wishes).row(back_to_menu)
    return keyboard


def ativity_markup():
    """"Кнопик для активностей"""
    events = KeyboardButton('Доступные мероприятия')
    place_in_rating = KeyboardButton('Я в рейтинге')
    know_someone_points = KeyboardButton('Узнать баллы человека')
    overall_rating = KeyboardButton('Общий рейтинг')
    back_to_menu = KeyboardButton('Вернуться в меню')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(events, overall_rating).row(place_in_rating, know_someone_points).row(back_to_menu)
    return keyboard


def guild_markup():
    """Кнопки для гита"""
    catering = KeyboardButton('Общепиты')
    places_to_relax = KeyboardButton('Места где можно отдохнуть')
    student_handbook = KeyboardButton('Справочник для первокурсника')
    back_to_menu = KeyboardButton('Вернуться в меню')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(student_handbook).row(catering, places_to_relax).row(back_to_menu)
    return keyboard


def todaytomorrow_markup():
    """Кнопки для Расписания (сегодня/завтра)"""
    today = KeyboardButton('Пары сегодня')
    tomorrow = KeyboardButton('Пары завтра')
    back_to_timetable = KeyboardButton('Вернуться в расписание')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(today, tomorrow).row(back_to_timetable)
    return keyboard


def someone_tametable_markup():
    """Кнопки для расписания (посмотреть расписание у другого человека)"""
    fi = KeyboardButton('Фамилия Имя')
    group = KeyboardButton('Номер группы')
    back_to_timetable = KeyboardButton('Вернуться в расписание')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(fi, group).row(back_to_timetable)
    return keyboard


def events_markup():
    copy_fio_group = KeyboardButton('Скопировать ФИО и группу')
    back_to_activity = KeyboardButton('Назад в активность')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(copy_fio_group).row(back_to_activity)
    return keyboard


def someone_points_markup():
    back_to_timetable = KeyboardButton('Назад в активность')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(back_to_timetable)
    return keyboard


def top_students_markup():
    top_1_10 = KeyboardButton('1-10 место')
    top_11_20 = KeyboardButton('11-20 место')
    top_21_30 = KeyboardButton('21-30 место')
    back_to_activity = KeyboardButton('Назад в активность')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(top_1_10, top_11_20, top_21_30).row(back_to_activity)
    return keyboard


def timetable_someone_markup():
    back_to_timetable = KeyboardButton('Вернуться в расписание')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(back_to_timetable)
    return keyboard


def wishes_markup():
    back_to_helps = KeyboardButton('Вернуться в помощь')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(back_to_helps)
    return keyboard
