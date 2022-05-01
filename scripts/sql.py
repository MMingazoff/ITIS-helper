import sqlite3
import os

"""Скрипты для БД"""
path = os.path.abspath(__file__)[:-14]
base = sqlite3.connect(path + 'data/students.db')
cursor = base.cursor()


def get_course(group: str) -> int:
    """Возвращает курс сутдента по его группе"""
    course = 1
    return course


def set_profile(user_id: int, fio: str) -> None:
    """Привязывает профиль к юзеру"""
    if user_in_db(user_id):
        cursor.execute("UPDATE users SET fio = ? WHERE user_id = ?", (fio, user_id))
    else:
        cursor.execute("INSERT INTO users (user_id, fio) VALUES (?,?)", (user_id, fio))
    base.commit()


def get_profile(user_id: int) -> str:
    """Возвращает ФИО студента, на который зашел юзер"""
    result = cursor.execute("SELECT fio FROM users WHERE user_id = ?", (user_id,))
    return result.fetchone()[0]


def user_in_db(user_id: int) -> bool:
    """Проверяет наличие пользователя в БД"""
    result = cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
    return bool(len(result.fetchall()))


def get_group(fio: str) -> str:
    """Возвращает группу студента по ФИО"""
    ...


def input_points(user_id: str, place: str) -> None:
    """Пользователь ставит баллы"""
    ...


def get_points(place: str) -> None:
    """Возвращает среднее количество баллов у места"""
    ...
