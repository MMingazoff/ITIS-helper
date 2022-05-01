from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from scripts.vk_parsing import MAX_POSTS


def menu_markup():
    """Кнопки для меню"""
    timetable = KeyboardButton('Расписание')
    study = KeyboardButton('Учеба')
    helps = KeyboardButton('Помощь')
    change_prof = KeyboardButton('Сменить профиль')
    activity = KeyboardButton('Активности')
    guide = KeyboardButton('Гид')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(timetable, change_prof).row(study, activity).row(helps, guide)
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


def study_markup(course: str):
    """Кнопки для учебы"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    back_to_menu = KeyboardButton('Назад в меню')
    course_dict = {
        'course_1': ['Информатика и программирование', 'Математический анализ', 'Алгебра и геометрия',
                     'Дискретная математика', 'Алгоритмы и структуры данных'],
        'course_2': ['Основы разработки информационных систем', 'Дисциплины по выбору Б1.В.ДВ.3'],
        'course_3': ['Программная инженерия', 'Архитектура программных систем', '	Информационная безопасность',
                     '	Управление проектами', 'Дисциплины по выбору Б1.В.ДВ.7'],
        'course_4': ['Основы информационного поиска', 'Дисциплины по выбору Б1.В.ДВ.12']}
    course = 'course_' + course
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


def activity_markup():
    """"Кнопик для активностей"""
    events = KeyboardButton('Доступные мероприятия')
    place_in_rating = KeyboardButton('Я в рейтинге')
    know_someone_points = KeyboardButton('Узнать баллы человека')
    overall_rating = KeyboardButton('Общий рейтинг')
    back_to_menu = KeyboardButton('Вернуться в меню')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(events, overall_rating).row(place_in_rating, know_someone_points).row(back_to_menu)
    return keyboard


def guide_markup():
    """Кнопки для гита"""
    catering = KeyboardButton('Общепиты')
    places_to_relax = KeyboardButton('Места где можно отдохнуть')
    student_handbook = KeyboardButton('Справочник для первокурсника')
    back_to_menu = KeyboardButton('Вернуться в меню')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(student_handbook).row(catering, places_to_relax).row(back_to_menu)
    return keyboard


def today_tomorrow_markup():
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


def events_inline_markup(post_url: str, post_num: int):
    url_button = InlineKeyboardButton(text='Ссылка на пост', url=post_url)
    next_post = InlineKeyboardButton(text='Следующий пост', callback_data=f'nextpost{post_num}')
    prev_post = InlineKeyboardButton(text='Предыдущий пост', callback_data=f'prevpost{post_num}')
    fio_copy = InlineKeyboardButton(text='Скопировать ФИО и группу', callback_data='copyfio')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(url_button)
    if post_num == 0:
        keyboard.add(next_post)
    elif post_num == MAX_POSTS - 1:
        keyboard.add(prev_post)
    else:
        keyboard.row(prev_post, next_post)
    keyboard.add(fio_copy)
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


def swap_profile_markup():
    back_to_menu = KeyboardButton('Вернуться в меню')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(back_to_menu)
    return keyboard

    
def delete_msg_inline_markup():
    """Инлайн кнопка, чтобы удалять сообщение"""
    delete_msg = InlineKeyboardButton(text='Удалить сообщение', callback_data='todelete')
    keyboard = InlineKeyboardMarkup()
    keyboard.add(delete_msg)
    return keyboard
