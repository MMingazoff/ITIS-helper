import os
import pandas as pd
from typing import List

"""Скрипты для excel"""

path = os.path.abspath(__file__)[:-16]
df_students = pd.read_excel(path + 'data/itis_students.xlsx')
list_groups = tuple(pd.read_excel(path + 'data/itis_groups.xlsx')['Group'])
df_exam = pd.read_excel(path + 'data/exam.xlsx')


def reload_data():
    """Обновляет данные"""
    global df_students, list_groups
    df_students = pd.read_excel(path + 'data/itis_students.xlsx')
    list_groups = tuple(pd.read_excel(path + 'data/itis_groups.xlsx')['Group'])


def is_a_student_by_fio(fio: str) -> bool:
    """Есть ли такой студент по ФИО"""
    if fio in tuple(df_students['FIO']):
        return True
    return False


def is_a_student_by_fi(fi: str) -> bool:
    """Есть ли такой студент по ФИ"""
    if fi in tuple(df_students['FI']):
        return True
    return False


def is_a_group(group_number: str) -> bool:
    """Есть ли такая группа"""
    if group_number in list_groups:
        return True
    return False


def get_fio_by_fi(fi: str) -> str:
    """Возвращает ФИО по ФИ"""
    profile = df_students[df_students['FI'] == fi]
    fio = tuple(profile['FIO'])[0]
    return str(fio)


def get_group_by_fi(fi: str) -> str:
    """Узнать группу по ФИ"""
    if is_a_student_by_fi(fi):
        profile = df_students[df_students['FI'] == fi]
        group = tuple(profile['Group'])[0]
        return str(group)
    return 'Такого студента нет'


def get_course_by_fi(fi: str) -> str:
    """Узнать курс по ФИ"""
    if is_a_student_by_fi(fi):
        profile = df_students[df_students['FI'] == fi]
        course = tuple(profile['Course'])[0]
        return str(course)
    return f'Такого студента нет'


def get_group_by_fio(fio: str) -> str:
    """Узнать группу по ФИО"""
    if is_a_student_by_fio(fio):
        profile = df_students[df_students['FIO'] == fio]
        group = tuple(profile['Group'])[0]
        return str(group)
    return f'Такого студента нет'


def get_all_group_members(group: str) -> List[str]:
    """Достает всех людей с группы"""
    members = df_students[df_students['Group'] == group]
    return list(members['FIO'])


def get_course_by_fio(fio: str) -> str:
    """Узнать курс по ФИО"""
    if is_a_student_by_fio(fio):
        profile = df_students[df_students['FIO'] == fio]
        course = tuple(profile['Course'])[0]
        return str(course)
    return f'Такого студента нет'


def from_du(fio: str) -> bool:
    profile = df_students[df_students['FIO'] == fio]
    return tuple(profile['from du'])[0]


def get_exam(group: str) -> str:
    """Узнать какие экзамены"""
    exams = df_exam[group].dropna()
    df_new = df_exam[df_exam[group].isin(exams)][['дни недели', 'дата', group]]
    result = df_new['дата'] + '(' + df_new['дни недели'] + '):</b></u>\n' + df_new[group] + '\n'
    return '\n'.join((f'<u><b>{exam}' for exam in result))
