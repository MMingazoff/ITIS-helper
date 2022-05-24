import sqlite3
import os
from scripts.excel import get_group_by_fi
from typing import List, Tuple

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


def get_everything(table: str) -> List[str]:
    """Достает все ссылки и из названия"""
    result = cursor.execute(f"SELECT * FROM {table}")
    return result.fetchall()


def add_link(name: str, link: str) -> bool:
    """Добавляет ссылку и название в БД"""
    try:
        cursor.execute("INSERT INTO links (name, link) VALUES (?,?)", (name, link))
        base.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def del_link(name: str) -> bool:
    """Удаляет ссылку из БД по названию"""
    result = cursor.execute("SELECT * FROM links WHERE name = ?", (name, ))
    cursor.execute("DELETE FROM links WHERE name = ?", (name, ))
    base.commit()
    return not bool(len(result.fetchall()))


def get_elders() -> List[Tuple[str, str, str]]:
    """Достает старост всех групп"""
    result = cursor.execute(f"SELECT * FROM elders")
    result = result.fetchall()
    result = [(get_group_by_fi(fi), fi, contact) for fi, contact in result]
    return result


def add_elder(fi: str, contact: str) -> bool:
    """Добавление старосты"""
    try:
        if get_group_by_fi(fi) == "Такого студента нет":
            return False
        cursor.execute("INSERT INTO elders (fi, contact) VALUES (?,?)", (fi, contact))
        base.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def del_elder(fi: str) -> bool:
    """Удаляет старосту из БД по имени"""
    result = cursor.execute("SELECT * FROM elders WHERE fi = ?", (fi, ))
    cursor.execute("DELETE FROM elders WHERE fi = ?", (fi,))
    base.commit()
    return bool(len(result.fetchall()))
