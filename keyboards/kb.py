from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from scripts.vk_parsing import MAX_POSTS
from scripts.sql import get_list_of_cafe, get_list_of_place


def menu_markup():
    """Кнопки для меню"""
    timetable = KeyboardButton('\U0001F4C5 Расписание')
    study = KeyboardButton('\U0001F4D5 Учеба')
    helps = KeyboardButton('\U0001F198 Помощь')
    change_prof = KeyboardButton('\U0001F503 Сменить профиль')
    activity = KeyboardButton('\U000026F3 Активности')
    guide = KeyboardButton('\U0001F5FA Гид')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(timetable, change_prof).row(study, activity).row(helps, guide)
    return keyboard


def timetable_markup():
    """Кнопки для расписания"""
    timetable_week = KeyboardButton('\U0001F4C5 Расписание на неделю')
    what_lesson_now = KeyboardButton('\U00002757 Какая у меня сейчас пара')
    timetable_day = KeyboardButton('\U00002753 Расписание на день')
    timetable_group = KeyboardButton('\U0001F50E Узнать пары у другого человека')
    back_to_menu = KeyboardButton('\U0001F519 Вернуться в меню')
    exam = KeyboardButton('✔ Мои экзамены')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(exam).row(timetable_week, timetable_day).row(what_lesson_now, timetable_group).row(back_to_menu)
    return keyboard


def study_markup(course: str):
    """Кнопки для учебы"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    back_to_menu = KeyboardButton('\U0001F519 Вернуться в меню')
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
    links = KeyboardButton('\U0001F517 Полезные ссылки')
    list_group = KeyboardButton('\U0001F46A Список моей группы')
    elders = KeyboardButton('\U0001F474 Список старост')
    wishes = KeyboardButton('\U0001F4EA Ваши пожелания для бота')
    back_to_menu = KeyboardButton('\U0001F519 Вернуться в меню')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(links, elders).row(list_group, wishes).row(back_to_menu)
    return keyboard


def activity_markup():
    """"Кнопик для активностей"""
    events = KeyboardButton('\U0000267F Доступные мероприятия')
    place_in_rating = KeyboardButton('\U0001F4C9 Узнать свое место в рейтинге')
    know_someone_points = KeyboardButton('\U0001F575 Узнать баллы человека')
    overall_rating = KeyboardButton('\U0001F51D Общий рейтинг')
    back_to_menu = KeyboardButton('\U0001F519 Вернуться в меню')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(events, overall_rating).row(place_in_rating, know_someone_points).row(back_to_menu)
    return keyboard


def guide_markup():
    """Кнопки для гита"""
    catering = KeyboardButton('\U0001F372 Общепиты')
    places_to_relax = KeyboardButton('\U0001F919 Места где можно отдохнуть')
    student_handbook = KeyboardButton('\U0001F64F Справочник для первокурсника')
    back_to_menu = KeyboardButton('\U0001F519 Вернуться в меню')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(student_handbook).row(catering, places_to_relax).row(back_to_menu)
    return keyboard


def today_tomorrow_markup():
    """Кнопки для Расписания (сегодня/завтра)"""
    today = KeyboardButton('Пары сегодня')
    tomorrow = KeyboardButton('Пары завтра')
    back_to_timetable = KeyboardButton('\U0001F519 Вернуться в расписание')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(today, tomorrow).row(back_to_timetable)
    return keyboard


def someone_timetable_markup():
    """Кнопки для расписания (посмотреть расписание у другого человека)"""
    fi = KeyboardButton('Фамилия Имя')
    group = KeyboardButton('Номер группы')
    back_to_timetable = KeyboardButton('\U0001F519 Вернуться в расписание')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(fi, group).row(back_to_timetable)
    return keyboard


def events_inline_markup(group_name: str, post_url: str, post_num: int):
    url_button = InlineKeyboardButton(text='Ссылка на пост', url=post_url)
    next_post = InlineKeyboardButton(text='Следующий пост', callback_data=f'{group_name}nextpost{post_num}')
    prev_post = InlineKeyboardButton(text='Предыдущий пост', callback_data=f'{group_name}prevpost{post_num}')
    copy_text = 'Скопировать ФИО и группу'
    call_back = 'copyfiogroup'
    if group_name == 'du':
        copy_text = 'Скопировать ФИО'
        call_back = 'copyfio'
    fio_copy = InlineKeyboardButton(text=copy_text, callback_data=call_back)
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
    back_to_timetable = KeyboardButton('\U0001F519 Вернуться в активность')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(back_to_timetable)
    return keyboard


def top_students_markup():
    top_1_10 = KeyboardButton('1-10 место')
    top_11_20 = KeyboardButton('11-20 место')
    top_21_30 = KeyboardButton('21-30 место')
    back_to_activity = KeyboardButton('\U0001F519 Вернуться в активность')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(top_1_10, top_11_20, top_21_30).row(back_to_activity)
    return keyboard


def timetable_someone_markup():
    back_to_timetable = KeyboardButton('\U0001F519 Вернуться в расписание')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(back_to_timetable)
    return keyboard


def wishes_markup():
    back_to_helps = KeyboardButton('\U0001F519 Вернуться в помощь')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(back_to_helps)
    return keyboard


def swap_profile_markup():
    back_to_menu = KeyboardButton('\U0001F519 Вернуться в меню')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(back_to_menu)
    return keyboard


def delete_msg_inline_markup():
    """Инлайн кнопка, чтобы удалять сообщение"""
    delete_msg = InlineKeyboardButton(text='Удалить сообщение', callback_data='todelete')
    keyboard = InlineKeyboardMarkup()
    keyboard.add(delete_msg)
    return keyboard


def choose_events_markup():
    itis_request = KeyboardButton('ITIS Request')
    du = KeyboardButton('ДУ 18')
    back_to_menu = KeyboardButton('\U0001F519 Вернуться в активность')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(itis_request, du).add(back_to_menu)
    return keyboard


def canteens_inline_markup():
    """Инлайн кнопка с общепитами"""
    canteens = get_list_of_cafe()
    keyboard = InlineKeyboardMarkup()
    for canteen in canteens:
        btn = InlineKeyboardButton(text=canteen, callback_data='canteen' + canteen)
        keyboard.add(btn)
    return keyboard


def places_inline_markup():
    """Инлайн кнопка с местдами для отдыха"""
    places = get_list_of_place()
    keyboard = InlineKeyboardMarkup()
    for place in places:
        btn = InlineKeyboardButton(text=place, callback_data='place' + place)
        keyboard.add(btn)
    return keyboard


def address_rating_inline_markup(address, name):
    """Инлайн кнопки: адрес, оценки"""
    keyboard = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text='Открыть в Google Maps', url=address)
    keyboard.add(btn)
    btn_mark_1 = InlineKeyboardButton('1️⃣', callback_data='1 point' + name)
    btn_mark_2 = InlineKeyboardButton('2️⃣', callback_data='2 point' + name)
    btn_mark_3 = InlineKeyboardButton('3️⃣', callback_data='3 point' + name)
    btn_mark_4 = InlineKeyboardButton('4️⃣', callback_data='4 point' + name)
    btn_mark_5 = InlineKeyboardButton('5️⃣', callback_data='5 point' + name)
    keyboard.row(btn_mark_1, btn_mark_2, btn_mark_3, btn_mark_4, btn_mark_5)
    return keyboard
