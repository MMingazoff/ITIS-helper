import openpyxl
import os


def get_students_balls():
    """Делает словарь {FIO: balls}"""
    path = os.path.abspath(__file__)[:-19]
    request_book = openpyxl.open(path + "data/request_active.xlsx", data_only=True)
    du_book = openpyxl.open(path + "data/du_active.xlsx", data_only=True)
    request_sheets = [request_book.worksheets[0], request_book.worksheets[1]]
    du_sheets = [du_book.worksheets[0]]
    request_book.close()
    du_book.close()
    students = dict()
    for sheet in request_sheets:
        for name, balls in sheet.iter_rows(min_row=6, min_col=2, max_col=3):
            students[name.value] = float(balls.value.replace(',', '.')) + students.get(name.value, 0)
    for name, balls in du_sheets[0].iter_rows(min_row=2, min_col=2, max_col=3):
        students[name.value] = float(balls.value.replace(',', '.')) + students.get(name.value, 0)
    return students


def sorted_balls():
    """Сортирует словарь баллов"""
    students = get_students_balls()
    sorted_students = \
        list(enumerate(sorted([(k, v) for k, v in students.items() if k], key=lambda el: el[1], reverse=True), 1))
    return sorted_students


def get_students_balls_place(sorted_students: list):
    """Изменяет словарь с {FIO: balls} на {FIO: (balls, place)}. То есть добавляет место в топе"""
    new_data = {}
    for place, (fio, balls) in sorted_students:
        new_data[fio] = (balls, place)
    return new_data
