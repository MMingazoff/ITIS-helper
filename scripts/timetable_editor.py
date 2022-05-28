from openpyxl import load_workbook
import pandas as pd
import os


def cell_to_row_column(cell):
    row = int(cell[1:]) - 2
    column = ord(cell[0]) - 64 - 1
    return row, column


def get_timetable(curse, name):
    wb = load_workbook(filename=path + 'timetable.xlsx', data_only=True)['1 курс']
    df = pd.read_excel(path + 'timetable.xlsx', sheet_name=['1 курс', '2 курс', '3 курс', '4 курс', 'Магистры'])
    merged_cells = wb.merged_cells.ranges
    df = df.get(curse)
    for i in merged_cells:
        cells = str(i)
        first_cell = cells.split(':')[0]
        second_cell = chr(ord(cells.split(':')[0][0]) + 1) + str(int(cells.split(':')[0][1:]))
        last_cell = cells.split(':')[1:2][0]
        first_cell_row, first_cell_column = cell_to_row_column(first_cell)
        last_cell_row, last_cell_column = cell_to_row_column(last_cell)
        if first_cell_row == last_cell_row and first_cell_column != last_cell_column:
            df.loc[first_cell_row][first_cell_column:last_cell_column + 1] = df.loc[first_cell_row][first_cell_column]
        else:
            for row in range(first_cell_row, last_cell_row + 1):
                df.loc[row][first_cell_column:last_cell_column + 1] = df.loc[first_cell_row][first_cell_column]
    df.to_excel(path+f'{name}.xlsx')


def get_edit_timetable(sheet_names):
    for key in sheet_names:
        get_timetable(key, sheet_names[key])


path = os.path.abspath(__file__)[:-27] + 'data/timetable/'
sheet = {
    '1 курс': '1course', '2 курс': '2course', '3 курс': '3course', '4 курс': '4course', 'Магистры': 'masters'}
get_edit_timetable(sheet)
