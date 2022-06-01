import openpyxl
import datetime
import os


def get_time_now():
    return datetime.datetime.now().time()


def check_time_in_range(start: datetime, end: datetime, current: datetime) -> bool:
    return start <= current <= end


def get_course(group: str) -> str:
    book = openpyxl.open(os.path.abspath(__file__)[:-20] + 'data/itis_groups.xlsx', read_only=True)
    sheet = book.active
    for index in range(2, 58):
        if sheet[index][0].value == group:
            return sheet[index][2].value
    book.close()


def get_index(group: str, sheet) -> int:
    for index in range(3, 14):
        if sheet[1][index].value == group:
            return index


def get_path(group: str) -> str:
    courses = {1: '1course.xlsx', 2: '2course.xlsx', 3: '3course.xlsx', 4: '4course.xlsx', 'Магистры': 'masters'}
    path = os.path.abspath(__file__)[:-20] + 'data/timetable/'
    return f'{path}{courses[get_course(group)]}'


def get_day_index() -> int:
    return datetime.datetime.today().weekday()


def get_lessons_by_day(group: str, sheet, day: int) -> str or bool:
    text = ''
    if day == 7:
        day = 0
    index = get_index(group, sheet)
    if day == 6:
        return 'Воскресенье - выходной день!'
    if day == 2 or day == 5:
        return 'Занятия по блоку дисциплин \n" Естественная-научная картина мира",' \
                    '\nсогласно приложению №3.'
    for i in range(2 + day * 7, day * 7 + 9):
        if sheet[i][index].value:
            text += f'**{str(sheet[i][2].value)}**\n{str(sheet[i][index].value)}\n'
    if len(text):
        return text
    return False


def get_week_timetable(group: str) -> tuple:
    book = openpyxl.open(get_path(group), read_only=True)
    sheet = book.active
    index_of_group = get_index(group, sheet)
    days = []
    for index_of_day in range(2, 44, 7):
        text = f'{sheet[index_of_day][1].value}\n'
        if (index_of_day == 16 or index_of_day == 37) and get_course(group) == 1:
            text += 'Занятия по блоку дисциплин \n" Естественная-научная картина мира",' \
                    '\nсогласно приложению №3.'
        else:
            for index in range(index_of_day, index_of_day+7):
                if sheet[index][index_of_group].value:
                    text += f'**{sheet[index][2].value}**\n{sheet[index][index_of_group].value}\n\n'
        if len(text) < 10:
            text += 'Нет пар'
        days.append(text)
    book.close()
    return days[0], days[1], days[2], days[3], days[4], days[5]


def get_now_lesson(group: str) -> str:
    time = get_time_now()
    book = openpyxl.open(get_path(group), read_only=True)
    sheet = book.active
    index = get_index(group, sheet)
    day = get_day_index()
    for i in range(2 + day * 7, day * 7 + 9):
        if sheet[i][index].value:
            if (i - 2) % 7 > 0:
                start_time = sheet[i-1][2].value[-5:]
            else:
                start_time = '08:00'
            start = datetime.time(int(start_time[:2]), int(start_time[-2:]))
            end_time = sheet[i][2].value[-5:]
            end = datetime.time(int(end_time[:2]), int(end_time[-2:]))
            if check_time_in_range(start, end, time):
                return f'**{sheet[i][2].value}**\n{sheet[i][index].value}'
    book.close()
    return 'у вас нет пары сейчас'


def get_today_lessons(group: str) -> str:
    book = openpyxl.open(get_path(group), read_only=True)
    sheet = book.active
    text = get_lessons_by_day(group, sheet, day=get_day_index())
    book.close()
    return text


def get_tomorrow_lessons(group: str) -> str:
    book = openpyxl.open(get_path(group), read_only=True)
    sheet = book.active
    text = get_lessons_by_day(group, sheet, day=get_day_index()+1)
    book.close()
    return text

