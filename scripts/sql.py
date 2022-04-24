"""Скрипты для БД"""


def get_course(group: str) -> int:
    """Возвращает курс сутдента по его группе"""
    course = 1
    return course


def get_profile(user_id: str) -> str:
    """Возвращает ФИО студента, на который зашел юзер"""
    ...


def get_group(fio: str) -> str:
    """Возвращает группу студента по ФИО"""
    ...


def set_profile(fio: str, user_id: str) -> None:
    """Привязывает профиль к юзеру"""
    ...


def input_points(user_id: str, place: str) -> None:
    """Пользователь ставит баллы"""
    ...


def get_points(place: str) -> None:
    """Возвращает среднее количество баллов у места"""
    ...
