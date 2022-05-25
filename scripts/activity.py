import openpyxl
import os


def get_data():
    path = os.path.abspath(__file__)[:-19]
    book = openpyxl.open(path + "data/activ.xlsx", data_only=True)
    book2 = openpyxl.open(path + "data/activ2.xlsx", data_only=True)
    sheets = [book.worksheets[1], book.worksheets[2]]
    sheets2 = [book2.worksheets[0]]
    data = {}
    for sheet in sheets:
        for name, balls in sheet.iter_rows(min_row=6, min_col=2, max_col=3):
            data[name.value] = balls.value + data.get(name.value, 0)
    for name, balls in sheets2[0].iter_rows(min_row=2, min_col=2, max_col=3):
        data[name.value] = balls.value + data.get(name.value, 0)
    return data


def sorted_balls():
    data = get_data()
    sorted_students = list(enumerate(sorted([(k,v) for k,v in data.items() if k], key=lambda el: el[1], reverse=True), 1))
    return sorted_students


def get_new_data():
    new_data = {}
    sorted_data = sorted_balls()
    for place, (fio, balls) in sorted_data:
        new_data[fio] = (balls, place)
    return new_data

