import openpyxl
import datetime
import os
def get_course(group):
    book = openpyxl.open(os.path.abspath(__file__)[:-20] + 'data/itis_groups.xlsx', read_only=True)
    sheet = book.active
    for index in range(2,58):
        if sheet[index][0].value == group:
            return sheet[index][2].value

def get_index(group,sheet):
    for index in range(3,14):
        if sheet[1][index].value == group:
            return index

def get_path(group):
    courses = {1:'1 курс.xlsx',2:'2 курс.xlsx',3:'3 курс.xlsx',4:'4 курс.xlsx','Магистры':'Магистры'}
    path = os.path.abspath(__file__)[:-20] + 'data/timetable/'
    return f'{path}{courses[get_course(group)]}'



def get_day_index():
    return datetime.datetime.today().weekday()

def get_lessons_by_day(group,sheet,day):
    text = ''
    index = get_index(group, sheet)
    if day == 6:
        return 'воскресенье - выходной день!'
    for i in range(2+ day*7 ,day *7 + 9):
        if sheet[i][index].value != None:
            text += f'{str(sheet[i][2].value)}\n{str(sheet[i][index].value)}\n'
    return text

def time_in_range(start, end, current):
    return start <= current <= end

def get_week_timetable(group: str) -> str:
    book = openpyxl.open(get_path(group), read_only=True)
    sheet = book.active
    monday = 'Понедельник\n'
    thues = 'Вторник\n'
    Wednesday = 'Среда\n'
    Thursday = 'Четверг\n'
    Friday=  'Пятница\n'
    Saturday = 'Суббота\n'
    days = [monday,thues,Wednesday,Thursday,Friday,Saturday]
    for index in range(len(days)):
        days[index] += get_lessons_by_day(group,sheet,index)
    return days[0],days[1],days[2],days[3],days[4],days[5]



def get_now_lesson(group: str) -> str:
    time = datetime.datetime.now().time()
    book = openpyxl.open(get_path(group), read_only=True)
    sheet = book.active
    index = get_index(group, sheet)
    day = get_day_index()
    for i in range(2+ day*7 ,day *7 + 9):
        if sheet[i][index].value != None:
            st = sheet[i][2].value[:5]
            start = datetime.time(int(st[:2]),int(st[-2:]))
            et = sheet[i][2].value[-5:]
            end = datetime.time(int(et[:2]),int(et[-2:]))
            if time_in_range(start,end,time):
                return sheet[i][index].value
    return 'у вас нет пары сейчас'

def get_today_lessons(group: str,day=get_day_index()) -> str:
    book = openpyxl.open(get_path(group), read_only=True)
    sheet = book.active
    return get_lessons_by_day(group,sheet,day)


def get_tomorrow_lessons(group: str) -> str:
    return get_today_lessons(group,day=get_day_index()+1)


def get_today_lessons_by_group(group: str):
    return get_today_lessons(group)
