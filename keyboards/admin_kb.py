from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_markup():
    useful_links = KeyboardButton('Полезные ссылки')
    elders = KeyboardButton('Список старост')
    cafes = KeyboardButton('Общепиты')
    leisure_places = KeyboardButton('Места для отдыха')
    stats = KeyboardButton('Краткая статистика')
    unban = KeyboardButton('Разбан')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(useful_links, elders).row(cafes, leisure_places).row(unban, stats)
    return keyboard


def interact_markup():
    to_add = KeyboardButton('Добавить')
    to_delete = KeyboardButton('Удалить')
    cancel = KeyboardButton('/cancel')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(to_add, to_delete).add(cancel)
    return keyboard


def cancel_markup():
    cancel = KeyboardButton('/cancel')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(cancel)
    return keyboard
