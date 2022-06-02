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
    result = result.fetchone()
    if result:
        return result[0]
    return ''


def user_in_db(user_id: int) -> bool:
    """Проверяет наличие пользователя в БД"""
    result = cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
    return bool(result.fetchall())


def get_group(fio: str) -> str:
    """Возвращает группу студента по ФИО"""
    ...


def set_points(user_id: str, place: str, points: int) -> None:
    """Пользователь ставит баллы"""
    cursor.execute(f"UPDATE users SET {place} = ? WHERE user_id = ?", (points, user_id))
    base.commit()


def get_points(place: str) -> str:
    """Возвращает среднее количество баллов у места"""
    avg = cursor.execute(f"SELECT AVG({place}) FROM users").fetchone()[0]
    if avg == 0:
        return 'Еще никто не голосовал'
    return f'Это место имеет среднюю оценку: {avg}'


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
    result = result.fetchall()
    cursor.execute("DELETE FROM links WHERE name = ?", (name, ))
    base.commit()
    return bool(result)


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


def add_cafe(name: str, description: str, address: str, photo: str) -> bool:
    """Добавляет общепит в БД"""
    try:
        cursor.execute("INSERT INTO canteens (name, description, address,photo) VALUES (?,?,?,?)",
                       (name, description, address, photo))
        base.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def add_place(name: str, description: str, address: str, photo: str) -> bool:
    """Добавляет место для отдыха в БД"""
    try:
        cursor.execute("INSERT INTO places (name, description, address,photo) VALUES (?,?,?,?)",
                       (name, description, address, photo))
        base.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def delete_cafe(name: str) -> bool:
    """Удаляет общепит по названию"""
    result = cursor.execute("SELECT * FROM canteens WHERE name = ?", (name,)).fetchone()
    cursor.execute("DELETE FROM canteens WHERE name = ?", (name,))
    base.commit()
    return bool(result)


def delete_place(name: str) -> bool:
    """Удаляет место для отдыха по названию"""
    result = cursor.execute("SELECT * FROM places WHERE name = ?", (name,)).fetchone()
    cursor.execute("DELETE FROM places WHERE name = ?", (name,))
    base.commit()
    return bool(result)


def get_list_of_cafe() -> list:
    """Список всех общепитов"""
    result = cursor.execute("SELECT name FROM canteens").fetchall()
    return [i[0] for i in result]


def get_list_of_place() -> list:
    """Список всех мест"""
    result = cursor.execute("SELECT name FROM places").fetchall()
    return [i[0] for i in result]


def del_elder(fi: str) -> bool:
    """Удаляет старосту из БД по имени"""
    result = cursor.execute("SELECT * FROM elders WHERE fi = ?", (fi, ))
    result = result.fetchall()
    cursor.execute("DELETE FROM elders WHERE fi = ?", (fi,))
    base.commit()
    return bool(result)


def get_total_users() -> int:
    """Возвращает количество пользователей"""
    result = cursor.execute("SELECT * FROM users")
    return len(result.fetchall())


def set_book(subject: str, title: str, link: str) -> None:
    """Добавляет книгу"""
    cursor.execute("INSERT INTO books (subject, title, link) VALUES (?,?)", (subject, title, link))


def get_books(subject: str) -> list:
    """Возвращает книгу"""
    books = cursor.execute("SELECT link, title FROM books WHERE subject = ?", (subject,)).fetchall()
    return books


def del_book(title: str) -> None:
    """Удаляет книгу"""
    cursor.execute("DELETE FROM books WHERE title = ?", (title,))


def get_canteen_description(name: str) -> str:
    """Описание общепита"""
    description = cursor.execute("SELECT description FROM canteens WHERE name = ?", (name,)).fetchone()[0]
    return description


def get_canteen_address(name: str) -> str:
    """Адрес общепита"""
    address = cursor.execute("SELECT address FROM canteens WHERE name = ?", (name,)).fetchone()[0]
    return address


def get_canteen_photo(name: str) -> str:
    """id фотографии общепита"""
    photo = cursor.execute("SELECT photo FROM canteens WHERE name = ?", (name,)).fetchone()[0]
    return photo


def get_place_description(name: str) -> str:
    """Описание места для отдыха"""
    description = cursor.execute("SELECT description FROM places WHERE name = ?", (name,)).fetchone()[0]
    return description


def get_place_address(name: str) -> str:
    """"Адрес места для отдыха"""
    address = cursor.execute("SELECT address FROM places WHERE name = ?", (name,)).fetchone()[0]
    return address


def get_place_photo(name: str) -> str:
    """id фотографии места для отдыха"""
    photo = cursor.execute("SELECT photo FROM places WHERE name = ?", (name,)).fetchone()[0]
    return photo


def add_column(name: str) -> None:
    """Добавление нового столбца в БД"""
    cursor.execute(f"ALTER TABLE users ADD column '{name.replace(' ', '')}' 'int'")
    base.commit()


def delete_column(name: str) -> None:
    """Удаление столбца из БД"""
    cursor.execute(f"ALTER TABLE users drop {name.replace(' ', '')}")
    base.commit()
